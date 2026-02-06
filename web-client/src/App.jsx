import React from 'react';
import Layout from './components/Layout';

function App() {
  return (
    <Layout>
      <div className="grid gap-6">
        {/* */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 text-center py-20">
          <h2 className="text-2xl font-semibold text-gray-800">Welcome to the Dashboard</h2>
          <p className="text-gray-500 mt-2">Upload a CSV file to get started.</p>
        </div>
      </div>
    </Layout>
  );
}

export default App;