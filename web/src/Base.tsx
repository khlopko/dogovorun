import {Content, Header} from "antd/lib/layout/layout";
import {Layout, Menu} from "antd";
import {Link} from "react-router-dom";
import React from "react";
import withRouter from "./withRouter";
import {green, grey} from "@ant-design/colors";
import {Footer} from "antd/es/layout/layout";

function Base(props: any) {
    return (
        <Layout style={{minHeight:"100vh"}}>
            <Header style={{ position: 'fixed', zIndex: 1, width: '100%', backgroundColor: green[5] }}>
                <Menu mode="horizontal" selectedKeys={[props.router.location.pathname]}>
                    <Menu.Item key="/">
                        <Link to="/">Бонд</Link>
                    </Menu.Item>
                    <Menu.Item key="/new">
                        <Link to="/new">Новая игра</Link>
                    </Menu.Item>
                </Menu>
            </Header>
            <Content className="site-layout" style={{ marginTop: 64 }}>
                <div className="site-layout-background" style={{ padding: 24, minHeight: 380 }}>
                    {props.children}
                </div>
            </Content>
            <Footer style={{ textAlign: 'center', backgroundColor: "white", color: green[6] }}>
                Бонд (с) 2022
            </Footer>
        </Layout>
    );
}

export default withRouter(Base);