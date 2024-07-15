import { useEffect, useState } from 'react';
import io from 'socket.io-client';

const useSocket = (url) => {
    const [header, setHeader] = useState('');
    const [text, setText] = useState('');
    const [data, setData] = useState([]);

    useEffect(() => {
        const socket = io(url);

        socket.on('FromAPI', (newData) => {
            if (newData && typeof newData === 'object') {
                setHeader(newData.header || '');
                setText(newData.text || '');
                setData((prevData) => [...prevData, ...newData.data]);
            }
        });

        return () => {
            socket.disconnect();
        };
    }, [url]);

    return { header, text, data };
};

export default useSocket;
