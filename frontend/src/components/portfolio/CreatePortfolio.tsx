
import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import { toast } from 'react-hot-toast';

const CreatePortfolio = () => {
    const { register, handleSubmit } = useForm();

    const onSubmit = async (data) => {
        try {
            await axios.post('/api/v1/portfolio', data);
            toast.success('Portfolio created successfully!');
        } catch (error) {
            toast.error('Error creating portfolio.');
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input {...register('name')} placeholder="Portfolio Name" />
            <button type="submit">Create Portfolio</button>
        </form>
    );
};

export default CreatePortfolio;
