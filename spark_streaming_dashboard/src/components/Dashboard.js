import React, { useEffect, useState } from 'react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';
import {
    Container, Grid, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Box
} from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme({
    palette: {
        background: {
            default: '#000000', // Black background
            paper: '#424242', // Dark grey for paper
            innerPaper: '#616161' // Lighter grey for inner content
        },
        text: {
            primary: '#FFFFFF', // White text for contrast
        },
    },
});

const Dashboard = () => {
    const [batchData, setBatchData] = useState([]);
    const [hatefulPercentage, setHatefulPercentage] = useState(0);
    const [offenders, setOffenders] = useState([]);
    const [totalMessages, setTotalMessages] = useState(0);
    const [totalHatefulMessages, setTotalHatefulMessages] = useState(0);
    const [topWords, setTopWords] = useState([]);
    const [top5ActiveUsers, setTop5ActiveUsers] = useState([]);

    useEffect(() => {
        const socket = new WebSocket('wss://deepwoke.com/ws');

        socket.onopen = () => {
            console.log('WebSocket connection opened');
        };

        socket.onmessage = (event) => {
            if (event.data instanceof Blob) {
                const reader = new FileReader();
                reader.onload = () => {
                    try {
                        const json = JSON.parse(reader.result);
                        console.log(json);
                        setBatchData(prevData => [
                            ...prevData,
                            {
                                timestamp: new Date(json.timestamp).toLocaleString(),
                                total: json.batchSize,
                                hateful: json.hatefulBatchSize
                            }
                        ]);
                        setHatefulPercentage(json.hateSpeechRatio);
                        setTotalMessages(json.totalMessages);
                        setTotalHatefulMessages(json.totalHatefulMessages);

                        if (json.top5Users) {
                            const sortedOffenders = json.top5Users.sort((a, b) => b.count - a.count); // Sort offenders by count in descending order
                            setOffenders(sortedOffenders);
                        }

                        if (json.top5ActiveUsers) {
                            const sortedActiveUsers = json.top5ActiveUsers.sort((a, b) => b.count - a.count); // Sort active users by count in descending order
                            setTop5ActiveUsers(sortedActiveUsers);
                        }

                        if (json.top10Words) {
                            setTopWords(json.top10Words);
                        }
                    } catch (e) {
                        console.error('Error parsing JSON:', e);
                    }
                };
                reader.readAsText(event.data);
            } else {
                console.log('Received:', event.data);
            }
        };

        socket.onclose = (event) => {
            console.log('WebSocket connection closed', event);
        };

        socket.onerror = (event) => {
            console.error('WebSocket error observed:', event);
        };

        return () => socket.close();
    }, []);

    const pieData = [
        { name: 'Hateful', value: hatefulPercentage * 100 },
        { name: 'Non-Hateful', value: 100 - (hatefulPercentage * 100) },
    ];

    const COLORS = ['#FF0000', '#008000'];

    const renderCustomizedLabel = ({ x, y, value }) => {
        return (
            <text x={x} y={y} fill="white" textAnchor="middle" dominantBaseline="central">
                {value.toFixed(1)}%
            </text>
        );
    };

    const customTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip" style={{ backgroundColor: '#333', padding: '10px', borderRadius: '5px', color: '#fff' }}>
                    <p>{`${payload[0].name} : ${payload[0].value.toFixed(1)}%`}</p>
                </div>
            );
        }

        return null;
    };

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Container style={{ backgroundColor: theme.palette.background.default, minHeight: '100vh', padding: '20px', display: 'flex', justifyContent: 'center' }}>
                <Paper style={{ padding: '20px', backgroundColor: theme.palette.background.paper }}>
                    <Typography variant="h4" align="center" gutterBottom style={{ color: theme.palette.text.primary }}>
                        WebSocket Dashboard
                    </Typography>
                    <Grid container spacing={3}>
                        <Grid item xs={12}>
                            <Paper elevation={3} style={{ backgroundColor: theme.palette.background.innerPaper }}>
                                <Typography variant="h6" align="center" gutterBottom style={{ color: theme.palette.text.primary }}>
                                    Messages Over Time
                                </Typography>
                                <div style={{ width: '100%', height: 400 }}>
                                    <ResponsiveContainer>
                                        <LineChart data={batchData}>
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="timestamp" stroke="#FFFFFF" />
                                            <YAxis stroke="#FFFFFF" />
                                            <Tooltip
                                                contentStyle={{ backgroundColor: '#FFFFFF', color: '#000000' }}
                                                itemStyle={{ color: '#000000' }}
                                            />
                                            <Legend />
                                            <Line type="monotone" dataKey="total" stroke="#FFFFFF" />
                                            <Line type="monotone" dataKey="hateful" stroke="#FF0000" />
                                        </LineChart>
                                    </ResponsiveContainer>

                                </div>
                            </Paper>
                        </Grid>
                        <Grid item xs={12}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <Paper elevation={3} style={{ flex: 1, marginRight: '10px', backgroundColor: theme.palette.background.innerPaper }}>
                                    <Typography variant="h6" align="center" gutterBottom style={{ color: theme.palette.text.primary }}>
                                        Hateful vs Non-Hateful Messages
                                    </Typography>
                                    <div style={{ width: '100%', height: 400 }}>
                                        <ResponsiveContainer>
                                            <PieChart>
                                                <Pie
                                                    data={pieData}
                                                    dataKey="value"
                                                    nameKey="name"
                                                    cx="50%"
                                                    cy="50%"
                                                    outerRadius={100}
                                                    fill="#8884d8"
                                                    label={renderCustomizedLabel}
                                                    labelLine={false}
                                                >
                                                    {pieData.map((entry, index) => (
                                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                                    ))}
                                                </Pie>
                                                <Tooltip content={customTooltip} />
                                            </PieChart>
                                        </ResponsiveContainer>
                                    </div>
                                    <Box display="flex" justifyContent="space-between" flexDirection={"column"} padding="10px">
                                        <Typography variant="h6" style={{ color: theme.palette.text.primary, paddingBottom:"20px" }}>
                                            Total Messages: {totalMessages}
                                        </Typography>

                                        <Typography variant="h6" style={{ color: theme.palette.text.primary }}>
                                            Total Hateful Messages: {totalHatefulMessages}
                                        </Typography>
                                    </Box>
                                </Paper>
                                <Paper elevation={3} style={{ flex: 1, marginLeft: '10px', backgroundColor: theme.palette.background.innerPaper }}>
                                    <Typography variant="h6" align="center" gutterBottom style={{ color: theme.palette.text.primary }}>
                                        Top Offenders
                                    </Typography>
                                    <TableContainer component={Paper} style={{ backgroundColor: theme.palette.background.innerPaper }}>
                                        <Table>
                                            <TableHead>
                                                <TableRow>
                                                    <TableCell style={{ color: theme.palette.text.primary }}>User</TableCell>
                                                    <TableCell align="right" style={{ color: theme.palette.text.primary }}>Hateful Messages</TableCell>
                                                </TableRow>
                                            </TableHead>
                                            <TableBody>
                                                {offenders.map((offender, index) => (
                                                    <TableRow key={index}>
                                                        <TableCell component="th" scope="row" style={{ color: theme.palette.text.primary }}>
                                                            {offender.user}
                                                        </TableCell>
                                                        <TableCell align="right" style={{ color: theme.palette.text.primary }}>{offender.count}</TableCell>
                                                    </TableRow>
                                                ))}
                                            </TableBody>
                                        </Table>
                                    </TableContainer>
                                    <Typography variant="h6" align="center" gutterBottom style={{ color: theme.palette.text.primary, marginTop: '10px' }}>
                                        Top 5 Active Users
                                    </Typography>
                                    <TableContainer component={Paper} style={{ backgroundColor: theme.palette.background.innerPaper }}>
                                        <Table>
                                            <TableHead>
                                                <TableRow>
                                                    <TableCell style={{ color: theme.palette.text.primary }}>User</TableCell>
                                                    <TableCell align="right" style={{ color: theme.palette.text.primary }}>Total Messages</TableCell>
                                                </TableRow>
                                            </TableHead>
                                            <TableBody>
                                                {top5ActiveUsers.map((user, index) => (
                                                    <TableRow key={index}>
                                                        <TableCell component="th" scope="row" style={{ color: theme.palette.text.primary }}>
                                                            {user.user}
                                                        </TableCell>
                                                        <TableCell align="right" style={{ color: theme.palette.text.primary }}>{user.count}</TableCell>
                                                    </TableRow>
                                                ))}
                                            </TableBody>
                                        </Table>
                                    </TableContainer>
                                </Paper>
                                <Paper elevation={3} style={{ flex: 1, marginLeft: '10px', backgroundColor: theme.palette.background.innerPaper }}>
                                    <Typography variant="h6" align="center" gutterBottom style={{ color: theme.palette.text.primary }}>
                                        Top 10 Words
                                    </Typography>
                                    <TableContainer component={Paper} style={{ backgroundColor: theme.palette.background.innerPaper }}>
                                        <Table>
                                            <TableHead>
                                                <TableRow>
                                                    <TableCell style={{ color: theme.palette.text.primary }}>Word</TableCell>
                                                    <TableCell align="right" style={{ color: theme.palette.text.primary }}>Count</TableCell>
                                                </TableRow>
                                            </TableHead>
                                            <TableBody>
                                                {topWords.map((word, index) => (
                                                    <TableRow key={index}>
                                                        <TableCell component="th" scope="row" style={{ color: theme.palette.text.primary }}>
                                                            {word.word}
                                                        </TableCell>
                                                        <TableCell align="right" style={{ color: theme.palette.text.primary }}>{word.count}</TableCell>
                                                    </TableRow>
                                                ))}
                                            </TableBody>
                                        </Table>
                                    </TableContainer>
                                </Paper>
                            </div>
                        </Grid>
                    </Grid>
                </Paper>
            </Container>
        </ThemeProvider>
    );
};

export default Dashboard;

