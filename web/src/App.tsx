import React from 'react';
import {Route, Routes} from "react-router-dom";
import Home from './Home';
import Base from "./Base";

import { ConfigProvider } from 'antd';
import { green } from "@ant-design/colors";
import Game from "./Game";

ConfigProvider.config({
  theme: {
    primaryColor: green[6],
  },
});

function App() {
    return (
        <Base>
            <Routes>
                <Route path='/' element={<Home />} />
                <Route path='/game/:id' element={<Game />} />
            </Routes>
        </Base>
    );
}

export default App;
