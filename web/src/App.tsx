import React from 'react';
import {Route, Routes} from "react-router-dom";
import Home from './Home';
import NewGame, {NewGameParameters} from "./NewGame";
import Base from "./Base";

import { ConfigProvider } from 'antd';
import { green } from "@ant-design/colors";

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
                <Route path='/new' element={<NewGame />} />
            </Routes>
        </Base>
    );
}

export default App;
