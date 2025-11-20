
import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Toaster, toast } from 'react-hot-toast';

const StatementsPage = () => {
  const [files, setFiles] = useState([]);
  const navigate = useNavigate();

  const onDrop = (acceptedFiles) => {
    setFiles(acceptedFiles);
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
        'application/pdf': ['.pdf'],
        'text/csv': ['.csv'],
    }
  });

  const handleUpload = async () => {
    if (files.length === 0) {
      toast.error('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', files[0]);

    try {
      const response = await axios.post('/api/v1/files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      toast.success('File uploaded successfully!');
      const { id } = response.data;
      await axios.post(`/api/v1/statements/process/${id}`);
      navigate(`/transactions/statement/${id}`);
    } catch (error) {
      toast.error('Error uploading file.');
    }
  };

  return (
    <div className="container mx-auto p-4">
        <Toaster />
      <h1 className="text-2xl font-bold mb-4">Upload Statement</h1>
      <div {...getRootProps()} className="border-2 border-dashed border-gray-400 p-8 text-center cursor-pointer">
        <input {...getInputProps()} />
        <p>Drag 'n' drop some files here, or click to select files</p>
      </div>
      {files.length > 0 && (
        <div className="mt-4">
          <h2 className="text-xl font-bold">Selected File:</h2>
          <ul>
            {files.map(file => (
              <li key={file.path}>{file.path} - {file.size} bytes</li>
            ))}
          </ul>
          <button
            onClick={handleUpload}
            className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Upload and Process
          </button>
        </div>
      )}
    </div>
  );
};

export default StatementsPage;
