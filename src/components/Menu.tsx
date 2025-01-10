import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/menu.scss';

const Menu: React.FC = () => {
    return (
        <div className="menu-container">
            <h1 className="menu-title">Real Time Viz</h1>
            <div className="menu-buttons">
                <Link to="/geo-1">
                    <button className="menu-button view1">Geographical View</button>
                </Link>
                <Link to="/geo-2">
                    <button className="menu-button view2">Placeholder</button>
                </Link>
                <Link to="/geo-3">
                    <button className="menu-button view3">Placeholder</button>
                </Link>
                <Link to="/graph">
                    <button className="menu-button view4">Placeholder</button>
                </Link>
            </div>
        </div>
    );
};

export default Menu;
