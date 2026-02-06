import React, { useState } from 'react';
import { UploadCloud, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { api } from '../services/api';

const FileUploader = ({ onUploadSuccess, compact = false }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      await api.uploadFile(file);
      setSuccess(true);
      onUploadSuccess();
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      console.error(err);
      setError("Failed. Check format.");
    } finally {
      setLoading(false);
    }
  };

  // Compact styles for sidebar widgets
  if (compact) {
      return (
        <div className="relative border-2 border-dashed border-slate-300 rounded-xl hover:border-blue-500 hover:bg-blue-50 transition-all group h-32 flex flex-col items-center justify-center text-center cursor-pointer">
            <input type="file" accept=".csv" onChange={handleFileChange} className="absolute inset-0 opacity-0 cursor-pointer z-10" disabled={loading} />
            {loading ? <Loader2 className="animate-spin text-blue-500" /> : 
             success ? <CheckCircle className="text-green-500" /> : 
             <UploadCloud className="text-slate-400 group-hover:text-blue-500" />}
            
            <p className="text-xs font-medium text-slate-600 mt-2">
                {loading ? "Uploading..." : success ? "Done!" : "Drop CSV here"}
            </p>
        </div>
      );
  }

  // Original Large Style (kept for "No Data" screen)
  return (
    <div className="mb-8">
      <div className="border-2 border-dashed border-slate-300 rounded-xl p-8 text-center hover:border-blue-500 hover:bg-blue-50 transition-colors relative group bg-white">
        <input 
          type="file" 
          accept=".csv"
          onChange={handleFileChange}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={loading}
        />
        <div className="flex flex-col items-center justify-center gap-3">
          {loading ? <Loader2 className="w-10 h-10 text-blue-600 animate-spin" /> : 
           success ? <CheckCircle className="w-10 h-10 text-green-500" /> : 
           <UploadCloud className="w-10 h-10 text-slate-400 group-hover:text-blue-500 transition-colors" />}
          
          <div className="space-y-1">
            <p className="font-medium text-slate-700">
              {loading ? "Processing..." : success ? "Upload Successful!" : "Click to upload or drag and drop"}
            </p>
            <p className="text-xs text-slate-500">CSV files only (max 10MB)</p>
          </div>
        </div>
      </div>
      {error && <p className="text-sm text-red-500 text-center mt-2">{error}</p>}
    </div>
  );
};

export default FileUploader;