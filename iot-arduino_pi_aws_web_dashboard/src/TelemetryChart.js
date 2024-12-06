import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
// Importera de komponenter som behövs från chart.js
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Registrera de nödvändiga komponenterna
ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Title, Tooltip, Legend);

const API_URL = 'https://rep1xcr4ol.execute-api.eu-north-1.amazonaws.com/amplify_api_stage/Items';

const TelemetryChart = () => {
  const [tempChartData, setTempChartData] = useState({});
  const [humidityChartData, setHumidityChartData] = useState({});
  const [loading, setLoading] = useState(true);

  const fetchTelemetryData = async () => {
    try {
      const response = await axios.get(API_URL, {
        headers: { Authorization: '11223344' },
      });

      const data = response.data.slice(-20); // Hämtar de senaste 20 mätningarna

      setTempChartData({
        labels: data.map((item) => new Date(item.timestamp).toLocaleTimeString()),
        datasets: [
          {
            label: 'Temperature (°C)',
            data: data.map((item) => item.temperature),
            borderColor: 'rgba(75,192,192,1)',
            backgroundColor: 'rgba(75,192,192,0.2)',
            fill: true,
          },
        ],
      });

      setHumidityChartData({
        labels: data.map((item) => new Date(item.timestamp).toLocaleTimeString()),
        datasets: [
          {
            label: 'Humidity (%)',
            data: data.map((item) => item.humidity),
            borderColor: 'rgba(153,102,255,1)',
            backgroundColor: 'rgba(153,102,255,0.2)',
            fill: true,
          },
        ],
      });

      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    fetchTelemetryData();
  }, []);

  return (
    <div className="chart-container">
      <h1 className="chart-title">Arduino R4 Wifi / DHT11 Sensor - Real Time</h1>
      <div className="chart-wrapper-container">
        <div className="chart-wrapper">
          <h3>Temperature</h3>
          {loading ? <p>Loading...</p> : <Line data={tempChartData} />}
        </div>
        <div className="chart-wrapper">
          <h3>Humidity</h3>
          {loading ? <p>Loading...</p> : <Line data={humidityChartData} />}
        </div>
      </div>
    </div>
  );
};

export default TelemetryChart;
