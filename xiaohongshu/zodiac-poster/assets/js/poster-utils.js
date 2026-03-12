/**
 * Poster Utils - 海报导出工具库
 *
 * 功能：将 HTML/SVG 海报导出为高清 PNG 图片
 * 技术：
 *   - HTML 模板：DOM → html2canvas → Canvas → PNG
 *   - SVG 模板：SVG → Image → Canvas → PNG（无需 html2canvas）
 *
 * 使用方式：
 * 1. 在 HTML 中引入此文件
 * 2. 调用 window.PosterUtils.exportPoster() 或 downloadPosters()
 */

(function() {
    'use strict';

    // 默认配置
    const DEFAULT_CONFIG = {
        scale: 2,           // 缩放倍数（2x = 2160x2880）
        format: 'png',      // 输出格式
        quality: 1.0,       // 图片质量（仅对 jpeg 有效）
        selector: '.poster',// 海报容器选择器（HTML 模板）
        svgSelector: 'svg', // SVG 选择器（SVG 模板）
        mode: 'auto'        // 导出模式：'auto' | 'html' | 'svg'
    };

    // 海报规格（小红书 3:4 比例）
    const POSTER_SIZE = {
        width: 1080,
        height: 1440
    };

    // SVG 模板规格（与 card-generator 一致的 3:4 比例，但更大）
    const SVG_SIZE = {
        width: 1080,
        height: 1440
    };

    /**
     * 等待所有图片和字体加载完成
     */
    async function waitForResources() {
        // 等待所有图片加载
        const images = document.querySelectorAll('img');
        const imagePromises = Array.from(images).map(img => {
            if (img.complete) return Promise.resolve();
            return new Promise((resolve, reject) => {
                img.onload = resolve;
                img.onerror = resolve; // 即使失败也继续
            });
        });

        // 等待字体加载
        if (document.fonts && document.fonts.ready) {
            await document.fonts.ready;
        }

        await Promise.all(imagePromises);

        // 额外等待渲染稳定
        await new Promise(resolve => setTimeout(resolve, 100));
    }

    /**
     * 检测元素类型（SVG 或 HTML）
     */
    function detectElementType(element) {
        if (element.tagName.toLowerCase() === 'svg') {
            return 'svg';
        }
        if (element.querySelector('svg') && !element.querySelector('.poster')) {
            return 'svg';
        }
        return 'html';
    }

    /**
     * SVG 元素 → Canvas（无需 html2canvas）
     * 参考 card-generator-skill 的实现
     */
    async function svgToCanvas(svgElement, scale = 2) {
        await waitForResources();

        // 克隆 SVG 以避免修改原始元素
        const svgClone = svgElement.cloneNode(true);

        // 确保 SVG 有正确的尺寸属性
        svgClone.setAttribute('width', SVG_SIZE.width);
        svgClone.setAttribute('height', SVG_SIZE.height);

        // 如果没有 viewBox，添加一个
        if (!svgClone.getAttribute('viewBox')) {
            svgClone.setAttribute('viewBox', `0 0 ${SVG_SIZE.width} ${SVG_SIZE.height}`);
        }

        // 序列化 SVG
        const svgString = new XMLSerializer().serializeToString(svgClone);
        const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(svgBlob);

        // 加载 SVG 为图片
        const img = new Image();
        await new Promise((resolve, reject) => {
            img.onload = resolve;
            img.onerror = reject;
            img.src = url;
        });

        // 创建 Canvas 并绘制（带缩放）
        const canvas = document.createElement('canvas');
        canvas.width = SVG_SIZE.width * scale;
        canvas.height = SVG_SIZE.height * scale;
        const ctx = canvas.getContext('2d');

        // 缩放绘制
        ctx.scale(scale, scale);
        ctx.drawImage(img, 0, 0);

        // 清理
        URL.revokeObjectURL(url);

        return canvas;
    }

    /**
     * HTML 元素 → Canvas
     * 使用 html2canvas 库（需要外部引入）
     */
    async function elementToCanvas(element, scale = 2) {
        if (typeof html2canvas === 'undefined') {
            throw new Error('html2canvas library is required. Please include it: <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>');
        }

        await waitForResources();

        const canvas = await html2canvas(element, {
            scale: scale,
            useCORS: true,
            allowTaint: true,
            backgroundColor: null,
            width: POSTER_SIZE.width,
            height: POSTER_SIZE.height,
            logging: false
        });

        return canvas;
    }

    /**
     * 智能导出：自动检测 SVG 或 HTML
     */
    async function smartToCanvas(element, scale = 2, mode = 'auto') {
        const type = mode === 'auto' ? detectElementType(element) : mode;

        if (type === 'svg') {
            const svg = element.tagName.toLowerCase() === 'svg'
                ? element
                : element.querySelector('svg');
            if (!svg) {
                throw new Error('No SVG element found');
            }
            return await svgToCanvas(svg, scale);
        } else {
            return await elementToCanvas(element, scale);
        }
    }

    /**
     * Canvas → Blob
     */
    function canvasToBlob(canvas, format = 'png', quality = 1.0) {
        return new Promise((resolve, reject) => {
            const mimeType = format === 'jpeg' ? 'image/jpeg' : 'image/png';
            canvas.toBlob(
                blob => blob ? resolve(blob) : reject(new Error('Failed to create blob')),
                mimeType,
                quality
            );
        });
    }

    /**
     * 下载单个文件
     */
    function downloadBlob(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    /**
     * 导出单张海报（支持 HTML 和 SVG）
     *
     * @param {Object} options - 配置选项
     * @param {HTMLElement} options.element - 要导出的元素（默认使用 .poster 或 svg）
     * @param {string} options.filename - 输出文件名
     * @param {number} options.scale - 缩放倍数
     * @param {string} options.format - 输出格式（png/jpeg）
     * @param {string} options.mode - 导出模式：'auto' | 'html' | 'svg'
     * @returns {Promise<Blob>} - 图片 Blob
     */
    async function exportPoster(options = {}) {
        const config = { ...DEFAULT_CONFIG, ...options };

        // 智能查找元素：先找 .poster（HTML），再找 svg（SVG）
        let element = config.element;
        if (!element) {
            element = document.querySelector(config.selector);
            if (!element) {
                element = document.querySelector(config.svgSelector);
            }
        }

        if (!element) {
            throw new Error(`Element not found: ${config.selector} or ${config.svgSelector}`);
        }

        const canvas = await smartToCanvas(element, config.scale, config.mode);
        const blob = await canvasToBlob(canvas, config.format, config.quality);

        if (config.filename) {
            downloadBlob(blob, config.filename);
        }

        return blob;
    }

    /**
     * 批量导出海报并打包为 ZIP
     *
     * @param {Array} posters - 海报配置数组 [{id, name, element?}, ...]
     * @param {string} zipFilename - ZIP 文件名
     * @param {Object} callbacks - 回调函数 {onStart, onProgress, onEnd, onError}
     */
    async function downloadPosters(posters, zipFilename, callbacks = {}) {
        const { onStart, onProgress, onEnd, onError } = callbacks;

        // 检查依赖
        if (typeof JSZip === 'undefined') {
            const error = new Error('JSZip library is required. Please include it: <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>');
            if (onError) onError(error);
            throw error;
        }

        if (typeof saveAs === 'undefined' && typeof FileSaver === 'undefined') {
            const error = new Error('FileSaver library is required. Please include it: <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>');
            if (onError) onError(error);
            throw error;
        }

        try {
            if (onStart) onStart();

            const zip = new JSZip();
            let processed = 0;

            for (const poster of posters) {
                const element = poster.element || document.getElementById(poster.id);

                if (!element) {
                    console.warn(`Poster element not found: ${poster.id}`);
                    continue;
                }

                const blob = await exportPoster({
                    element: element,
                    scale: poster.scale || DEFAULT_CONFIG.scale,
                    format: poster.format || DEFAULT_CONFIG.format,
                    mode: poster.mode || DEFAULT_CONFIG.mode
                });

                const filename = `${poster.name || poster.id}.png`;
                zip.file(filename, blob);

                processed++;
                if (onProgress) onProgress(processed, posters.length);
            }

            const content = await zip.generateAsync({ type: 'blob' });

            // 使用 FileSaver 或 saveAs
            const save = typeof saveAs !== 'undefined' ? saveAs : FileSaver.saveAs;
            save(content, zipFilename);

            if (onEnd) onEnd();

        } catch (error) {
            console.error('Export failed:', error);
            if (onError) onError(error);
            throw error;
        }
    }

    /**
     * 创建导出按钮并添加到页面
     *
     * @param {Object} options - 按钮配置
     */
    function createExportButton(options = {}) {
        const {
            text = '导出图片',
            loadingText = '导出中...',
            position = 'bottom-right',
            className = '',
            onClick = null
        } = options;

        const button = document.createElement('button');
        button.textContent = text;
        button.className = `poster-export-btn ${className}`;

        // 默认样式
        const style = document.createElement('style');
        style.textContent = `
            .poster-export-btn {
                position: fixed;
                ${position.includes('bottom') ? 'bottom: 20px;' : 'top: 20px;'}
                ${position.includes('right') ? 'right: 20px;' : 'left: 20px;'}
                padding: 12px 24px;
                background: #C4653A;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                z-index: 9999;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(196, 101, 58, 0.3);
            }
            .poster-export-btn:hover {
                background: #A85432;
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(196, 101, 58, 0.4);
            }
            .poster-export-btn:disabled {
                background: #999;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
        `;
        document.head.appendChild(style);

        button.addEventListener('click', async () => {
            if (button.disabled) return;

            button.disabled = true;
            button.textContent = loadingText;

            try {
                if (onClick) {
                    await onClick();
                } else {
                    // 默认行为：导出当前页面的 .poster 元素
                    const filename = document.title.replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_') + '.png';
                    await exportPoster({ filename });
                }
            } catch (error) {
                alert('导出失败: ' + error.message);
            } finally {
                button.disabled = false;
                button.textContent = text;
            }
        });

        document.body.appendChild(button);
        return button;
    }

    // 暴露到全局
    window.PosterUtils = {
        // 主要 API
        exportPoster,
        downloadPosters,
        createExportButton,
        // 底层 API
        smartToCanvas,
        svgToCanvas,
        elementToCanvas,
        canvasToBlob,
        downloadBlob,
        waitForResources,
        detectElementType,
        // 常量
        POSTER_SIZE,
        SVG_SIZE,
        DEFAULT_CONFIG
    };

    // 兼容 CommonJS
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = window.PosterUtils;
    }

})();
