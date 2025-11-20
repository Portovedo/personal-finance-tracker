
import React from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import { toast } from 'react-hot-toast';

const AddHolding = ({ portfolioId }) => {
    const { register, handleSubmit } = useForm();

    const onSubmit = async (data) => {
        try {
            await axios.post(`/api/v1/portfolio/${portfolioId}/holdings`, data);
            toast.success('Holding added successfully!');
        } catch (error) {
            toast.error('Error adding holding.');
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <input {...register('symbol')} placeholder="Symbol" />
            <input {...register('quantity')} placeholder="Quantity" type="number" step="any" />
            <input {...register('avg_cost')} placeholder="Average Cost" type="number" step="any" />
            <button type="submit">Add Holding</button>
        </form>
    );
};

export default AddHolding;
