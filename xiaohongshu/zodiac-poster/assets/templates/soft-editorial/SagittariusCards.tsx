import React, { useState } from 'react';

/*
 * 设计方向: Soft Editorial - 温柔有态度
 * 手机优化: 单栏居中、超大字体、清晰层次
 * 尺寸: 1080 x 1440px (3:4)
 */

const colors = {
  cream: '#faf9f5',
  warmCream: '#f5f2ea',
  dark: '#1a1918',
  charcoal: '#2d2b29',
  midGray: '#9a958c',
  lightGray: '#e5e2db',
  orange: '#d97757',
  orangeLight: '#e8a08a',
  blue: '#6a9bcc',
  green: '#788c5d',
  brown: '#7a7265',
};

// 磨砂颗粒质感
const GrainTexture = () => (
  <div
    className="absolute inset-0 pointer-events-none z-40"
    style={{
      backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
      opacity: 0.35,
      mixBlendMode: 'overlay',
    }}
  />
);

// 射手座符号
const SagittariusIcon = ({ size = 100, color = colors.orange }) => (
  <svg width={size} height={size} viewBox="0 0 100 100" fill="none">
    <path
      d="M20 80 L80 20 M60 20 L80 20 L80 40 M25 55 L55 25"
      stroke={color}
      strokeWidth="4"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

// 摩羯座符号
const CapricornIcon = ({ size = 80, color = colors.midGray }) => (
  <svg width={size} height={size} viewBox="0 0 100 100" fill="none">
    <path
      d="M28 28 C28 28 22 52 34 64 C46 76 58 76 58 86 C58 94 50 94 44 90 M58 86 C58 86 74 80 80 64 C86 48 74 36 58 36 C42 36 36 48 36 60"
      stroke={color}
      strokeWidth="4"
      strokeLinecap="round"
      fill="none"
    />
  </svg>
);

// 双鱼座符号
const PiscesIcon = ({ size = 80, color = colors.blue }) => (
  <svg width={size} height={size} viewBox="0 0 100 100" fill="none">
    <path
      d="M20 20 C38 32 38 68 20 80 M80 20 C62 32 62 68 80 80 M15 50 L85 50"
      stroke={color}
      strokeWidth="4"
      strokeLinecap="round"
    />
  </svg>
);

// 天蝎座符号
const ScorpioIcon = ({ size = 80, color = colors.orange }) => (
  <svg width={size} height={size} viewBox="0 0 100 100" fill="none">
    <path
      d="M16 20 L16 70 C16 80 26 80 26 70 L26 20 M36 20 L36 70 C36 80 46 80 46 70 L46 20 M56 20 L56 70 C56 80 66 75 72 65 L82 75 M76 65 L82 75 L72 82"
      stroke={color}
      strokeWidth="4"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

// 页面容器
const Page = ({ children, bg = 'cream' }) => {
  const backgrounds = {
    cream: `linear-gradient(180deg, ${colors.cream} 0%, ${colors.warmCream} 100%)`,
    dark: `linear-gradient(180deg, ${colors.dark} 0%, ${colors.charcoal} 100%)`,
  };

  return (
    <div
      className="relative overflow-hidden"
      style={{
        width: '1080px',
        height: '1440px',
        background: backgrounds[bg],
      }}
    >
      {children}
      <GrainTexture />
    </div>
  );
};

// ========== 封面 - 情感冲击力 ==========
const Cover = () => (
  <Page bg="cream">
    {/* 顶部橙色条 */}
    <div className="absolute top-0 left-0 right-0 h-2" style={{ backgroundColor: colors.orange }} />

    {/* 大背景符号 */}
    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-[0.04]">
      <SagittariusIcon size={800} color={colors.dark} />
    </div>

    {/* 主内容 - 居中布局 */}
    <div className="absolute inset-0 flex flex-col items-center justify-center px-16">
      {/* 小标签 */}
      <div
        className="px-8 py-3 mb-12"
        style={{ backgroundColor: colors.orange }}
      >
        <span
          className="text-xl tracking-[0.3em]"
          style={{ color: colors.cream, fontFamily: "'Outfit', sans-serif", fontWeight: 500 }}
        >
          射手座专属
        </span>
      </div>

      {/* 主标题 - 超大情感化 */}
      <h1
        className="text-center leading-[1.1] mb-8"
        style={{
          fontSize: '100px',
          color: colors.dark,
          fontFamily: "'Noto Serif SC', serif",
          fontWeight: 600,
        }}
      >
        射手座
        <br />
        最容易<span style={{ color: colors.orange }}>栽</span>的
        <br />
        3个星座
      </h1>

      {/* 副标题 - 情感共鸣 */}
      <p
        className="text-center text-3xl leading-relaxed mt-8 mb-16"
        style={{ color: colors.brown, fontFamily: "'Noto Serif SC', serif" }}
      >
        情劫都在这里了
      </p>

      {/* 分隔线 */}
      <div className="flex items-center gap-6 mb-8">
        <div className="w-20 h-[2px]" style={{ backgroundColor: colors.orange, opacity: 0.6 }} />
        <SagittariusIcon size={40} color={colors.orange} />
        <div className="w-20 h-[2px]" style={{ backgroundColor: colors.orange, opacity: 0.6 }} />
      </div>

      {/* 提示 */}
      <p
        className="text-xl tracking-[0.2em]"
        style={{ color: colors.midGray, fontFamily: "'Outfit', sans-serif" }}
      >
        向左滑动 →
      </p>
    </div>

    {/* 底部装饰 */}
    <div className="absolute bottom-12 left-1/2 -translate-x-1/2 flex gap-3">
      {[1,2,3,4,5,6,7].map(i => (
        <div
          key={i}
          className="w-2 h-2 rounded-full"
          style={{ backgroundColor: i === 1 ? colors.orange : colors.lightGray }}
        />
      ))}
    </div>
  </Page>
);

// ========== 第1页 - 情劫引入 ==========
const Page1 = () => (
  <Page bg="cream">
    {/* 页码 */}
    <div
      className="absolute top-16 left-16 w-14 h-14 rounded-full flex items-center justify-center"
      style={{ backgroundColor: colors.orange }}
    >
      <span className="text-xl font-semibold" style={{ color: colors.cream, fontFamily: "'Outfit', sans-serif" }}>01</span>
    </div>

    {/* 主内容 - 绝对居中 */}
    <div className="absolute inset-0 flex flex-col items-center justify-center px-20">
      {/* 小标题 */}
      <p
        className="text-2xl tracking-[0.4em] mb-6"
        style={{ color: colors.brown, fontFamily: "'Outfit', sans-serif" }}
      >
        射手的
      </p>

      {/* 大标题 */}
      <h1
        className="text-[160px] mb-12"
        style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif", fontWeight: 600 }}
      >
        情劫
      </h1>

      {/* 内容文字 - 大字体易读 */}
      <div
        className="text-center text-4xl leading-[2]"
        style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif", opacity: 0.85 }}
      >
        <p>射手不轻易动心</p>
        <p>但一旦栽了</p>
        <p>就栽得<span className="font-semibold" style={{ color: colors.orange }}>很彻底</span></p>
      </div>

      {/* 引言框 */}
      <div
        className="mt-20 px-12 py-8"
        style={{ backgroundColor: colors.dark }}
      >
        <p
          className="text-2xl italic text-center"
          style={{ color: colors.cream, fontFamily: "'Noto Serif SC', serif" }}
        >
          "不撞南墙不回头，是我没错了"
        </p>
      </div>
    </div>
  </Page>
);

// ========== TOP3 摩羯座 ==========
const Page2 = () => (
  <Page bg="cream">
    {/* 大号背景数字 */}
    <div
      className="absolute top-20 right-16 text-[280px] font-light leading-none opacity-[0.06]"
      style={{ color: colors.dark, fontFamily: "'Outfit', sans-serif" }}
    >
      03
    </div>

    {/* TOP标签 */}
    <div
      className="absolute top-16 left-16 px-6 py-3"
      style={{ backgroundColor: colors.midGray }}
    >
      <span className="text-lg font-semibold" style={{ color: colors.cream, fontFamily: "'Outfit', sans-serif" }}>TOP 3</span>
    </div>

    {/* 主内容 */}
    <div className="absolute inset-0 flex flex-col items-center justify-center px-16">
      {/* 星座符号 */}
      <CapricornIcon size={100} color={colors.midGray} />

      {/* 星座名 */}
      <h1
        className="text-[120px] mt-6 mb-2"
        style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif", fontWeight: 600 }}
      >
        摩羯座
      </h1>

      <p
        className="text-lg tracking-[0.5em] mb-10"
        style={{ color: colors.midGray, fontFamily: "'Outfit', sans-serif" }}
      >
        CAPRICORN
      </p>

      {/* 关键词 */}
      <div
        className="px-16 py-5 mb-12"
        style={{ border: `3px solid ${colors.midGray}`, borderRadius: '60px' }}
      >
        <span
          className="text-4xl tracking-widest"
          style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif" }}
        >
          冷淡
        </span>
      </div>

      {/* 说明文字 */}
      <div
        className="text-center text-3xl leading-[2.2]"
        style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif", opacity: 0.8 }}
      >
        <p>越得不到越想要</p>
        <p>越被忽视越<span className="font-semibold" style={{ color: colors.orange }}>上头</span></p>
        <p className="mt-4" style={{ color: colors.brown }}>最后受伤的，永远是射手</p>
      </div>

      {/* 底部引言 */}
      <div className="absolute bottom-24 left-1/2 -translate-x-1/2">
        <p
          className="text-2xl italic"
          style={{ color: colors.brown, fontFamily: "'Noto Serif SC', serif" }}
        >
          "你的冷漠，是我的砒霜"
        </p>
      </div>
    </div>
  </Page>
);

// ========== TOP2 双鱼座 ==========
const Page3 = () => (
  <Page bg="cream">
    {/* 大号背景数字 */}
    <div
      className="absolute top-20 left-16 text-[280px] font-light leading-none opacity-[0.05]"
      style={{ color: colors.blue, fontFamily: "'Outfit', sans-serif" }}
    >
      02
    </div>

    {/* TOP标签 */}
    <div
      className="absolute top-16 right-16 px-6 py-3"
      style={{ backgroundColor: colors.blue }}
    >
      <span className="text-lg font-semibold" style={{ color: colors.cream, fontFamily: "'Outfit', sans-serif" }}>TOP 2</span>
    </div>

    {/* 主内容 */}
    <div className="absolute inset-0 flex flex-col items-center justify-center px-16">
      {/* 星座符号 */}
      <PiscesIcon size={100} color={colors.blue} />

      {/* 星座名 */}
      <h1
        className="text-[120px] mt-6 mb-2"
        style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif", fontWeight: 600 }}
      >
        双鱼座
      </h1>

      <p
        className="text-lg tracking-[0.5em] mb-10"
        style={{ color: colors.blue, fontFamily: "'Outfit', sans-serif" }}
      >
        PISCES
      </p>

      {/* 关键词 */}
      <div
        className="px-16 py-5 mb-12"
        style={{ backgroundColor: colors.blue, borderRadius: '60px' }}
      >
        <span
          className="text-4xl tracking-widest"
          style={{ color: colors.cream, fontFamily: "'Noto Serif SC', serif" }}
        >
          深情
        </span>
      </div>

      {/* 说明文字 */}
      <div
        className="text-center text-3xl leading-[2.2]"
        style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif", opacity: 0.8 }}
      >
        <p>爱得太满太重</p>
        <p>射手喘不过气</p>
        <p className="mt-4">想逃又舍不得</p>
        <p>最后成了<span className="font-semibold" style={{ color: colors.orange }}>渣</span></p>
      </div>

      {/* 底部引言 */}
      <div className="absolute bottom-24 left-1/2 -translate-x-1/2">
        <p
          className="text-2xl italic"
          style={{ color: colors.brown, fontFamily: "'Noto Serif SC', serif" }}
        >
          "不是不爱，是承受不起"
        </p>
      </div>
    </div>
  </Page>
);

// ========== TOP1 天蝎座 - 深色突出 ==========
const Page4 = () => (
  <Page bg="dark">
    {/* 超大背景数字 */}
    <div
      className="absolute -top-10 -right-10 text-[400px] font-light leading-none opacity-[0.04]"
      style={{ color: colors.orange, fontFamily: "'Outfit', sans-serif" }}
    >
      01
    </div>

    {/* TOP标签 */}
    <div
      className="absolute top-16 left-16 px-8 py-4"
      style={{ backgroundColor: colors.orange }}
    >
      <span className="text-xl font-semibold" style={{ color: colors.cream, fontFamily: "'Outfit', sans-serif" }}>TOP 1</span>
    </div>

    {/* 主内容 */}
    <div className="absolute inset-0 flex flex-col items-center justify-center px-16">
      {/* 星座符号 */}
      <ScorpioIcon size={120} color={colors.orange} />

      {/* 星座名 */}
      <h1
        className="text-[140px] mt-6 mb-2"
        style={{ color: colors.orange, fontFamily: "'Noto Serif SC', serif", fontWeight: 600 }}
      >
        天蝎座
      </h1>

      <p
        className="text-lg tracking-[0.5em] mb-10"
        style={{ color: colors.midGray, fontFamily: "'Outfit', sans-serif" }}
      >
        SCORPIO
      </p>

      {/* 关键词 */}
      <div
        className="px-16 py-5 mb-12"
        style={{ border: `3px solid ${colors.orange}`, borderRadius: '60px' }}
      >
        <span
          className="text-4xl tracking-widest"
          style={{ color: colors.orange, fontFamily: "'Noto Serif SC', serif" }}
        >
          控制欲
        </span>
      </div>

      {/* 说明文字 */}
      <div
        className="text-center text-3xl leading-[2.2]"
        style={{ color: colors.lightGray, fontFamily: "'Noto Serif SC', serif" }}
      >
        <p>天蝎的控制欲</p>
        <p>和射手的自由天生相克</p>
        <p className="mt-4">又爱又恨，互相折磨</p>
        <p>明知不合适，就是<span className="font-semibold" style={{ color: colors.orange }}>断不掉</span></p>
      </div>

      {/* 底部引言 */}
      <div
        className="absolute bottom-24 left-1/2 -translate-x-1/2 px-12 py-6"
        style={{ backgroundColor: colors.orange }}
      >
        <p
          className="text-2xl italic"
          style={{ color: colors.cream, fontFamily: "'Noto Serif SC', serif" }}
        >
          "你是我戒不掉的毒"
        </p>
      </div>
    </div>
  </Page>
);

// ========== 第5页 - 成长 ==========
const Page5 = () => (
  <Page bg="cream">
    {/* 装饰圆环 */}
    <div
      className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full opacity-[0.06]"
      style={{ border: `40px solid ${colors.green}` }}
    />

    {/* 页码 */}
    <div
      className="absolute top-16 left-16 px-6 py-3"
      style={{ backgroundColor: colors.green }}
    >
      <span className="text-lg font-semibold" style={{ color: colors.cream, fontFamily: "'Outfit', sans-serif" }}>GROWTH</span>
    </div>

    {/* 主内容 */}
    <div className="absolute inset-0 flex flex-col items-center justify-center px-20">
      {/* 标题 */}
      <h1
        className="text-[120px] mb-16"
        style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif", fontWeight: 600 }}
      >
        栽过之后
      </h1>

      {/* 内容卡片 */}
      <div
        className="px-16 py-14"
        style={{ backgroundColor: colors.cream, boxShadow: '0 8px 60px rgba(0,0,0,0.06)' }}
      >
        <div
          className="text-center text-4xl leading-[2]"
          style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif" }}
        >
          <p>射手栽过跟头</p>
          <p>才学会<span className="font-semibold" style={{ color: colors.green }}>保护自己</span></p>
          <p className="mt-8" style={{ opacity: 0.7 }}>不是变冷漠了</p>
          <p style={{ opacity: 0.7 }}>是学会了看清</p>
        </div>
      </div>

      {/* 引言 */}
      <div className="mt-16 flex items-center gap-6">
        <div className="w-12 h-[2px]" style={{ backgroundColor: colors.green }} />
        <p
          className="text-3xl"
          style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif" }}
        >
          "痛过才知道，什么值得"
        </p>
        <div className="w-12 h-[2px]" style={{ backgroundColor: colors.green }} />
      </div>
    </div>
  </Page>
);

// ========== 结尾页 ==========
const EndPage = () => (
  <Page bg="cream">
    {/* 大背景符号 */}
    <div className="absolute top-40 left-1/2 -translate-x-1/2 opacity-[0.06]">
      <SagittariusIcon size={400} color={colors.dark} />
    </div>

    {/* 主内容 */}
    <div className="absolute inset-0 flex flex-col items-center justify-center px-16">
      {/* 小标题 */}
      <p
        className="text-xl tracking-[0.4em] mb-4"
        style={{ color: colors.brown, fontFamily: "'Outfit', sans-serif" }}
      >
        写给射手
      </p>

      {/* 主标题 */}
      <h1
        className="text-center text-[88px] leading-[1.2] mb-12"
        style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif", fontWeight: 600 }}
      >
        愿你被
        <br />
        <span style={{ color: colors.orange }}>温柔以待</span>
      </h1>

      {/* 内容 */}
      <div
        className="text-center text-3xl leading-[2.2] mb-16"
        style={{ color: colors.dark, fontFamily: "'Noto Serif SC', serif", opacity: 0.8 }}
      >
        <p>每一次<span style={{ color: colors.orange }}>受伤</span></p>
        <p>都是成长的代价</p>
        <p className="mt-6">愿你下一次心动</p>
        <p>不再是<span style={{ color: colors.orange }}>情劫</span></p>
        <p className="mt-6" style={{ opacity: 0.7 }}>而是对的人，在对的时间出现</p>
      </div>

      {/* 分隔线 */}
      <div className="w-24 h-[2px] mb-12" style={{ backgroundColor: colors.orange }} />

      {/* CTA */}
      <div className="text-center">
        <p
          className="text-2xl mb-3"
          style={{ color: colors.brown, fontFamily: "'Noto Serif SC', serif" }}
        >
          点赞 · 收藏 · 关注
        </p>
        <p
          className="text-lg"
          style={{ color: colors.midGray, fontFamily: "'Outfit', sans-serif" }}
        >
          更多星座内容，敬请期待
        </p>
      </div>
    </div>

    {/* 底部装饰 */}
    <div className="absolute bottom-12 left-1/2 -translate-x-1/2 flex gap-3">
      {[1,2,3,4,5,6,7].map(i => (
        <div
          key={i}
          className="w-2 h-2 rounded-full"
          style={{ backgroundColor: i === 7 ? colors.orange : colors.lightGray }}
        />
      ))}
    </div>
  </Page>
);

// ========== 主组件 ==========
export default function SagittariusCards() {
  const [current, setCurrent] = useState(0);

  const pages = [
    { component: Cover, name: '封面' },
    { component: Page1, name: '情劫' },
    { component: Page2, name: 'TOP3' },
    { component: Page3, name: 'TOP2' },
    { component: Page4, name: 'TOP1' },
    { component: Page5, name: '成长' },
    { component: EndPage, name: '结尾' },
  ];

  const CurrentPage = pages[current].component;

  return (
    <div className="min-h-screen py-8" style={{ backgroundColor: '#252422' }}>
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Outfit:wght@300;400;500;600&display=swap');
        `}
      </style>

      {/* 标题 */}
      <div className="text-center mb-6">
        <h1
          className="text-xl mb-2 tracking-widest"
          style={{ color: colors.cream, fontFamily: "'Outfit', sans-serif" }}
        >
          射手座情劫 · 小红书
        </h1>
        <p style={{ color: colors.midGray, fontSize: '14px' }}>
          1080 × 1440px · 3:4 竖图 · 手机友好设计
        </p>
      </div>

      {/* 导航 */}
      <div className="flex justify-center gap-2 mb-8 flex-wrap px-4">
        {pages.map((page, i) => (
          <button
            key={i}
            onClick={() => setCurrent(i)}
            className="px-4 py-2 text-sm transition-all"
            style={{
              backgroundColor: current === i ? colors.orange : colors.lightGray,
              color: current === i ? colors.cream : colors.dark,
              fontFamily: "'Outfit', sans-serif",
              fontWeight: 500,
            }}
          >
            {page.name}
          </button>
        ))}
      </div>

      {/* 页面展示 - 缩放适配 */}
      <div className="flex justify-center overflow-auto pb-8">
        <div
          style={{
            transform: 'scale(0.45)',
            transformOrigin: 'top center',
            boxShadow: '0 30px 100px rgba(0,0,0,0.5)',
          }}
        >
          <CurrentPage />
        </div>
      </div>

      {/* 页码 */}
      <div className="flex justify-center gap-3 mt-[-200px]">
        {pages.map((_, i) => (
          <div
            key={i}
            onClick={() => setCurrent(i)}
            className="w-3 h-3 rounded-full cursor-pointer transition-all"
            style={{
              backgroundColor: current === i ? colors.orange : colors.midGray,
              opacity: current === i ? 1 : 0.4,
            }}
          />
        ))}
      </div>
    </div>
  );
}
