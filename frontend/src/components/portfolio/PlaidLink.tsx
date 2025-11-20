import React, { useCallback, useState, useEffect } from 'react';
import { usePlaidLink } from 'react-plaid-link';
import axios from 'axios';

const PlaidLink = () => {
    const [linkToken, setLinkToken] = useState(null);

    const createLinkToken = async () => {
        try {
            const response = await axios.post('/api/v1/portfolio/plaid/create-link-token');
            setLinkToken(response.data.link_token);
        } catch (error) {
            console.error("Error creating link token", error);
        }
    };

    useEffect(() => {
        createLinkToken();
    }, []);

    const onSuccess = useCallback((public_token: string, metadata: any) => {
        axios.post('/api/v1/portfolio/plaid/exchange-public-token', { public_token });
    }, []);

    const onExit = useCallback((err: any, metadata: any) => {
        // handle exit
        if (err) console.error(err);
    }, []);

    const config = {
        token: linkToken,
        onSuccess,
        onExit,
    };

    const { open, ready } = usePlaidLink(config);

    return (
        <button 
            onClick={() => open()} 
            disabled={!ready}
            className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
        >
            Connect a bank account
        </button>
    );
};

export default PlaidLink;