import { X, AlertTriangle } from 'lucide-react';

interface DisclaimerBannerProps {
  data: {
    primary_disclaimer: string;
    glucose_response: string;
    medical_conditions: string[];
    limitations: string[];
  };
  onDismiss: () => void;
}

export default function DisclaimerBanner({ data, onDismiss }: DisclaimerBannerProps) {
  return (
    <div className="bg-brand-primary text-white p-4 shadow-lg">
      <div className="container-responsive">
        <div className="flex gap-4 items-start">
          <AlertTriangle className="flex-shrink-0 mt-1" size={24} />
          <div className="flex-1">
            <h3 className="font-bold text-lg mb-2">Important Disclaimer</h3>
            <p className="text-sm mb-3">{data.primary_disclaimer}</p>
            <p className="text-sm mb-3">{data.glucose_response}</p>

            <div className="grid md:grid-cols-2 gap-4 text-sm mb-4">
              <div>
                <p className="font-semibold mb-2">Medical Conditions:</p>
                <ul className="list-disc list-inside space-y-1">
                  {data.medical_conditions.slice(0, 2).map((cond, idx) => (
                    <li key={idx}>{cond}</li>
                  ))}
                </ul>
              </div>
              <div>
                <p className="font-semibold mb-2">Limitations:</p>
                <ul className="list-disc list-inside space-y-1">
                  {data.limitations.slice(0, 2).map((lim, idx) => (
                    <li key={idx}>{lim}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
          <button
            onClick={onDismiss}
            className="flex-shrink-0 hover:bg-white hover:bg-opacity-20 p-1 rounded-lg transition"
            aria-label="Close disclaimer"
          >
            <X size={24} />
          </button>
        </div>
      </div>
    </div>
  );
}

