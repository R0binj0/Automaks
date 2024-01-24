"use client"

import { useState } from "react";

export default function Home() {

  const [numberPlate, setNumberPlate] = useState('');
  const [loading, setLoading] = useState(false);
  const [aastamaks, setAastamaks] = useState(null);
  const [showClientText, setShowClientText] = useState(false);

  const handleCalculate = async () => {
    setLoading(true);

    try {
      const response = await fetch('/api/python', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ registration_mark: numberPlate }),
      });

      const result = await response.json();
      console.log(result);

      setAastamaks(result.aastamaks);
      setShowClientText(true);
    } catch (error) {
      console.error('Error during calculation:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-cover"> 
      <div className="flex flex-col justify-center w-1/2 m-auto">
        <div className="bg-white w-100">
          <div className="text-9xl text-gray-400 flex justify-center py-10">
            <i className="truck icon"></i>
          </div>
          <div className="flex justify-center flex-col gap-4">
            <div className="text-5xl text-blue-600">Numbri märk</div>
            <input className="text-5xl p-2 border-2 border-solid border-gray-400 rounded-md" placeholder="123 ABC" value={numberPlate} onChange={(e) => setNumberPlate(e.target.value)}></input>
          </div>
          <div className="flex justify-center flex-col gap-4">
            {loading ? (
              <div className="text-5xl flex justify-center text-gray-400">Loading...</div>
            ) : (
              <>
                {showClientText && (
                  <>
                    <div className="text-9xl text-gray-400 flex justify-center py-10">
                      <i className="calculator icon"></i>
                    </div>
                    <div className="text-5xl text-blue-600">Antud sõiduki aastamaks on {aastamaks !== null ? `${aastamaks}€` : ''}</div>
                  </>
                )}
              </>
            )}
          </div>
          <button className="bg-blue-500 text-white text-5xl w-full p-2 mt-4" onClick={handleCalculate}>
            Calculate
          </button>
        </div>
      </div>
    </div>
  )
}
