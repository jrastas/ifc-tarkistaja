/**
 * Toggle between viewing required only or all fields.
 */

interface ViewModeToggleProps {
  viewMode: 'required' | 'all';
  onViewModeChange: (mode: 'required' | 'all') => void;
}

export function ViewModeToggle({
  viewMode,
  onViewModeChange,
}: ViewModeToggleProps) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-slate-600">Näytä:</span>
      <div className="flex bg-slate-100 rounded-lg p-1">
        <button
          onClick={() => onViewModeChange('required')}
          className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
            viewMode === 'required'
              ? 'bg-white text-slate-800 shadow-sm'
              : 'text-slate-600 hover:text-slate-800'
          }`}
        >
          Pakolliset
        </button>
        <button
          onClick={() => onViewModeChange('all')}
          className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
            viewMode === 'all'
              ? 'bg-white text-slate-800 shadow-sm'
              : 'text-slate-600 hover:text-slate-800'
          }`}
        >
          Kaikki
        </button>
      </div>
    </div>
  );
}
