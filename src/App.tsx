import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Menu from './components/Menu';
import GeoView1 from './components/GeoView1';
import StockDisplay from './components/StockDisplay';
import GeoView3 from './components/GeoView3';
import GraphView from './components/ArtVisCollaborationNetwork';
import './styles/app.scss';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Menu />} />
                <Route path="/geo-1" element={<GeoView1 />} />
                <Route path="/Stock-2" element={<StockDisplay />} />
                <Route path="/geo-3" element={<GeoView3 />} />
                <Route path="/graph" element={<GraphView />} />
            </Routes>
        </Router>
    );
}

export default App;
