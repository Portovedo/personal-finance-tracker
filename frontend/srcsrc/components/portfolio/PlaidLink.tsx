
import React, { useCallback, useState } from 'react';
import { usePlaidLink } from 'react-plaid-link';
import axios from 'axios';

const PlaidLink = () => {
    const [linkToken, setLinkToken] = useState(null);

    const onSuccess = useCallback((public_token, metadata) => {
        axios.post('/api/v1/portfolio/plaid/exchange-public-token', { public_token });
    }, []);

    const onExit = useCallback((err, metadata) => {
        // handle exit
    }, []);

    const config = {
        token: linkToken,
        onSuccess,
        onExit,
    };

    const { open, ready } = usePlaidLink(config);

    const createLinkToken = async () => {
        const response = await axios.post('/api/v1/portfolio/plaid/create-link-token');
        setLinkToken(response.data.link_token);
    };

    React.useEffect(() => {
        createLinkToken();
    }, []);

    return (
        <button onClick={() => open()} disabled={!ready}>
            Connect a bank account
        </button>
    );
};

export default PlaidLink;
