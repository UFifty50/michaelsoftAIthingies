import { StrictMode } from 'react';
import * as ReactDOMClient from 'react-dom/client';
import './styles.scss';
import 'dockview/dist/styles/dockview.css';

import Container from './app';

const rootElement = document.getElementById('root');

if (rootElement) {
    const root = ReactDOMClient.createRoot(rootElement);

    root.render(
        <StrictMode>
            <div className="app">
                <Container />
            </div>
        </StrictMode>
    );
}
