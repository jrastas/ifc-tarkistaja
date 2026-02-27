/**
 * SVG circular progress indicator for compliance percentage.
 */

interface ComplianceGaugeProps {
  percentage: number;
  label: string;
  size?: 'sm' | 'md' | 'lg';
}

export function ComplianceGauge({
  percentage,
  label,
  size = 'md',
}: ComplianceGaugeProps) {
  const sizes = {
    sm: { width: 80, stroke: 6, fontSize: 'text-lg' },
    md: { width: 120, stroke: 8, fontSize: 'text-2xl' },
    lg: { width: 160, stroke: 10, fontSize: 'text-3xl' },
  };

  const { width, stroke, fontSize } = sizes[size];
  const radius = (width - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = Math.min(Math.max(percentage, 0), 100);
  const offset = circumference - (progress / 100) * circumference;

  // Color based on percentage
  const getColor = (pct: number) => {
    if (pct >= 90) return 'text-green-500';
    if (pct >= 70) return 'text-amber-500';
    return 'text-red-500';
  };

  const getStrokeColor = (pct: number) => {
    if (pct >= 90) return 'stroke-green-500';
    if (pct >= 70) return 'stroke-amber-500';
    return 'stroke-red-500';
  };

  return (
    <div className="flex flex-col items-center">
      <div className="relative" style={{ width, height: width }}>
        <svg
          className="transform -rotate-90"
          width={width}
          height={width}
        >
          {/* Background circle */}
          <circle
            cx={width / 2}
            cy={width / 2}
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth={stroke}
            className="text-slate-200"
          />
          {/* Progress circle */}
          <circle
            cx={width / 2}
            cy={width / 2}
            r={radius}
            fill="none"
            strokeWidth={stroke}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className={`transition-all duration-500 ${getStrokeColor(progress)}`}
          />
        </svg>
        {/* Percentage text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={`font-bold ${fontSize} ${getColor(progress)}`}>
            {progress.toFixed(0)}%
          </span>
        </div>
      </div>
      <span className="mt-2 text-sm text-slate-600 text-center">{label}</span>
    </div>
  );
}
