window.CardUtils = {
    /**
     * Download SVGs as PNGs in a ZIP file
     * @param {Array<{id: string, name: string}>} cards - List of cards to process
     * @param {string} filename - Output zip filename
     * @param {Object} callbacks - Lifecycle callbacks
     */
    downloadCards: async (cards, filename, callbacks = {}) => {
        const { onStart, onEnd, onError, onProgress } = callbacks;
        if (onStart) onStart();

        try {
            if (typeof JSZip === 'undefined' || typeof saveAs === 'undefined') {
                throw new Error('Required libraries (JSZip, FileSaver) not loaded');
            }

            const zip = new JSZip();
            let processedCount = 0;
            
            for (const card of cards) {
                const container = document.getElementById(card.id);
                const svg = container?.querySelector('svg');
                if (!svg) {
                    console.warn(`Card container/SVG not found for id: ${card.id}`);
                    continue;
                }

                // Clone SVG to manipulate it without affecting the display
                const svgClone = svg.cloneNode(true);
                
                // Ensure standard size for export
                svgClone.setAttribute('width', '300');
                svgClone.setAttribute('height', '400');
                
                // Embed fonts if needed - for simplest usage we skip complex font embedding 
                // and rely on system fonts or browser rendering.
                
                const svgString = new XMLSerializer().serializeToString(svgClone);
                const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
                const url = URL.createObjectURL(svgBlob);

                const img = new Image();
                await new Promise((resolve, reject) => {
                    img.onload = resolve;
                    img.onerror = reject;
                    img.src = url;
                });

                const canvas = document.createElement('canvas');
                // 4x resolution for high quality
                canvas.width = 1200;
                canvas.height = 1600;
                const ctx = canvas.getContext('2d');
                
                // Clear and set white background (optional, but good for transparency safety)
                // ctx.fillStyle = '#ffffff';
                // ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                ctx.scale(4, 4);
                ctx.drawImage(img, 0, 0);

                const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
                zip.file(`${card.name}.png`, blob);
                URL.revokeObjectURL(url);
                
                processedCount++;
                if (onProgress) onProgress(processedCount, cards.length);
            }

            const content = await zip.generateAsync({ type: 'blob' });
            saveAs(content, filename);
        } catch (error) {
            console.error('Export failed:', error);
            if (onError) onError(error);
            else alert('Download failed: ' + error.message);
        } finally {
            if (onEnd) onEnd();
        }
    }
};
