import { Activity, ShieldCheck, TrendingUp } from 'lucide-react';
import { Simulation } from '@/types';

interface MetabolicAvatarProps {
  simulation: Simulation;
}

export default function MetabolicAvatar({ simulation }: MetabolicAvatarProps) {
  const fatEstimate = simulation.fat_storage_estimate;
  const storageHigh = fatEstimate.potential_fat_storage_g_high;
  const state =
    simulation.storage_risk_score >= 70 || storageHigh >= 25
      ? 'elevated'
      : simulation.storage_risk_score >= 40 || storageHigh >= 10
        ? 'moderate'
        : 'balanced';

  const config = {
    balanced: {
      title: 'Balanced response',
      message: 'Your educational avatar is handling this meal with lower storage pressure.',
      color: 'bg-brand-secondary',
      icon: ShieldCheck,
    },
    moderate: {
      title: 'Moderate storage pressure',
      message: 'Your educational avatar shows some surplus-energy storage pressure.',
      color: 'bg-energy-storage',
      icon: Activity,
    },
    elevated: {
      title: 'Elevated storage pressure',
      message: 'Your educational avatar shows higher estimated storage pressure for this meal context.',
      color: 'bg-energy-risk',
      icon: TrendingUp,
    },
  }[state];

  const Icon = config.icon;

  return (
    <div className="grid lg:grid-cols-[220px,1fr] gap-8 items-center bg-brand-light border border-gray-100 rounded-lg p-6">
      <div className="flex justify-center">
        <div className="relative w-40 h-52">
          <div className={`absolute left-1/2 top-0 -translate-x-1/2 w-20 h-20 ${config.color} rounded-full shadow-sm`} />
          <div className={`absolute left-1/2 top-16 -translate-x-1/2 w-28 h-32 ${config.color} rounded-[2rem] shadow-sm`} />
          <div className="absolute left-[3.2rem] top-8 w-3 h-3 bg-white rounded-full" />
          <div className="absolute right-[3.2rem] top-8 w-3 h-3 bg-white rounded-full" />
          <div className="absolute left-1/2 top-28 -translate-x-1/2 w-16 h-16 rounded-full border-4 border-white border-opacity-80 flex items-center justify-center text-white">
            <Icon size={26} />
          </div>
          <div className="absolute left-2 top-24 w-10 h-4 bg-brand-dark rounded-full rotate-[-32deg]" />
          <div className="absolute right-2 top-24 w-10 h-4 bg-brand-dark rounded-full rotate-[32deg]" />
        </div>
      </div>

      <div>
        <p className="text-sm font-semibold text-brand-primary mb-2">Educational metabolic avatar</p>
        <h3 className="text-2xl font-bold mb-3">{config.title}</h3>
        <p className="text-gray-700 mb-4">{config.message}</p>
        <div className="grid sm:grid-cols-3 gap-3">
          <div className="bg-white rounded-lg border border-gray-100 p-4">
            <p className="text-xs font-semibold text-gray-500 mb-1">Possible surplus</p>
            <p className="text-xl font-bold">{fatEstimate.estimated_energy_surplus_kcal.toFixed(0)} kcal</p>
          </div>
          <div className="bg-white rounded-lg border border-gray-100 p-4">
            <p className="text-xs font-semibold text-gray-500 mb-1">Fat equivalent</p>
            <p className="text-xl font-bold">
              {fatEstimate.potential_fat_storage_g_low.toFixed(1)}-{fatEstimate.potential_fat_storage_g_high.toFixed(1)}g
            </p>
          </div>
          <div className="bg-white rounded-lg border border-gray-100 p-4">
            <p className="text-xs font-semibold text-gray-500 mb-1">Activity offset</p>
            <p className="text-xl font-bold">{fatEstimate.activity_offset_kcal.toFixed(0)} kcal</p>
          </div>
        </div>
        <p className="text-xs text-gray-600 mt-4">{fatEstimate.assumption}</p>
      </div>
    </div>
  );
}
