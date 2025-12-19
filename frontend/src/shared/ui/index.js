export const cn = (...classes) => classes.filter(Boolean).join(' ');

export const gradients = {
  shell: 'bg-[linear-gradient(145deg,#fff1f8,#f1f5ff)]',
  mark: 'bg-[linear-gradient(135deg,#7c2cf3,#ff5aa5)]',
  dropzone:
    'bg-[radial-gradient(circle_at_20%_20%,#e7fbff,transparent_60%),linear-gradient(135deg,#fff2f8,#f1f5ff)]',
};

export const layout = {
  page: 'min-h-screen px-4 py-8 app-background text-ink',
  container: 'mx-auto max-w-5xl space-y-5',
  stack: 'space-y-3',
};

export const branding = {
  mark: `grid h-14 w-14 place-items-center rounded-2xl border-3 border-ink ${gradients.mark} text-white shadow-ink-md text-lg font-extrabold tracking-wide`,
};

export const surfaces = {
  shell: `px-6 py-5 rounded-3xl border-4 border-ink ${gradients.shell} shadow-ink-lg`,
  panel: 'p-6 rounded-3xl border-4 border-ink bg-paper shadow-ink-md',
  message: 'p-4 rounded-2xl border-3 border-ink bg-white/90 shadow-ink-sm',
  muted: 'p-4 rounded-2xl border-3 border-ink/80 bg-paper-muted text-ink/70 shadow-ink-sm text-center',
};

export const chips = {
  purple: 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border-2 border-ink bg-brand-purple text-white shadow-ink-sm text-xs font-semibold',
  cyan: 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border-2 border-ink bg-brand-cyan text-ink shadow-ink-sm text-xs font-semibold',
  pink: 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border-2 border-ink bg-brand-pink text-white shadow-ink-sm text-xs font-semibold',
  gold: 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border-2 border-ink bg-brand-gold text-ink shadow-ink-sm text-xs font-semibold',
  orange: 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border-2 border-ink bg-brand-orange text-white shadow-ink-sm text-xs font-semibold',
};

export const pills = {
  statusBase: 'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-semibold',
  statusOk: 'border-2 border-ink bg-emerald-300 text-ink shadow-ink-sm',
  statusWarn: 'border-2 border-ink bg-amber-300 text-ink shadow-ink-sm',
  file: 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full border-2 border-ink bg-brand-purple text-white shadow-ink-sm text-sm font-semibold',
  cache: 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full border-2 border-ink bg-brand-cyan text-ink shadow-ink-sm text-sm font-semibold',
  fileItem: 'inline-flex items-center gap-2 rounded-2xl border-2 border-ink bg-white text-ink shadow-ink-sm text-sm',
  fileItemCompact: 'px-3 py-1',
  fileItemLoose: 'px-3 py-2',
  source: 'px-2.5 py-1 rounded-full border-2 border-ink bg-brand-gold text-ink shadow-ink-sm text-xs font-semibold uppercase tracking-wide',
};

export const buttons = {
  primary:
    'inline-flex h-11 items-center justify-center px-5 rounded-full border-2 border-ink bg-brand-purple text-white shadow-ink-md text-sm font-semibold transition-transform hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-ink-sm disabled:cursor-not-allowed disabled:border-ink/30 disabled:bg-slate-200 disabled:text-slate-500 disabled:shadow-none',
  accent:
    'inline-flex h-10 items-center justify-center px-4 rounded-full border-2 border-ink bg-brand-pink text-white shadow-ink-md text-sm font-semibold transition-transform hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-ink-sm',
  upload:
    'relative inline-flex h-11 cursor-pointer items-center justify-center px-4 rounded-full border-2 border-ink bg-brand-cyan text-ink shadow-ink-md text-sm font-semibold transition-transform hover:-translate-y-0.5 active:translate-x-0.5 active:translate-y-0.5 active:shadow-ink-sm',
  icon:
    'grid h-6 w-6 place-items-center rounded-full border-2 border-ink bg-brand-pink text-white shadow-ink-sm text-xs font-bold transition-transform hover:-translate-y-0.5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-cyan/40',
};

export const textStyles = {
  label: 'text-ink font-semibold',
  subtext: 'text-ink/70 text-sm',
  caption: 'text-ink/60 text-xs uppercase tracking-[0.08em]',
  muted: 'text-ink/60',
  warning: 'text-amber-700 text-sm',
};

export const inputs = {
  textarea:
    'min-h-[140px] resize-y px-4 py-3 rounded-2xl border-3 border-ink bg-white text-ink placeholder:text-ink/50 shadow-ink-sm text-base outline-none transition focus:border-brand-purple focus:shadow-ink-md focus:ring-0',
  dropzone:
    `px-4 py-4 rounded-2xl border-3 border-dashed border-ink ${gradients.dropzone} shadow-ink-sm transition hover:-translate-y-0.5 hover:border-brand-purple hover:shadow-ink-md`,
};
