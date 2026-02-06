import React from 'react';

const DataTable = ({ data }) => {
  if (!data || data.length === 0) return null;

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
      <div className="p-6 border-b border-gray-100">
        <h3 className="text-lg font-semibold text-gray-800">Equipment Data Logs</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-gray-600">
          <thead className="bg-gray-50 text-gray-900 font-medium">
            <tr>
              <th className="px-6 py-4">ID</th>
              <th className="px-6 py-4">Equipment Name</th>
              <th className="px-6 py-4">Type</th>
              <th className="px-6 py-4">Flowrate (m³/h)</th>
              <th className="px-6 py-4">Pressure (bar)</th>
              <th className="px-6 py-4">Temp (°C)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {data.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 font-medium text-gray-900">{item.equipment_id}</td>
                <td className="px-6 py-4">{item.name}</td>
                <td className="px-6 py-4">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {item.type}
                  </span>
                </td>
                <td className="px-6 py-4">{item.flowrate}</td>
                <td className="px-6 py-4">{item.pressure}</td>
                <td className="px-6 py-4">{item.temperature}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;