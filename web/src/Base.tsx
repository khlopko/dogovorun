import {Content, Header} from "antd/lib/layout/layout";
import {Layout, Menu} from "antd";
import {Link} from "react-router-dom";
import React from "react";
import withRouter, {RouterProps} from "./withRouter";
import {green} from "@ant-design/colors";
import {Footer} from "antd/es/layout/layout";
import {create} from "./api";

function Base(props: any) {
    return (
        <Layout style={{minHeight:"100vh"}}>
            <Header style={{ position: 'fixed', zIndex: 1, width: '100%', backgroundColor: green[5] }}>
                <Menu mode="horizontal" selectedKeys={[props.router.location.pathname]}>
                    <Menu.Item key="/">
                        <Link to="/">Бонд</Link>
                    </Menu.Item>
                    <Menu.Item key="/new">
                        <a onClick={() => newGame(props)}>Новая игра</a>
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

function newGame(props: RouterProps) {
    create().then(result => {
        if (result.ok) {
            props.router?.navigate(`/game/${result.value}`)
        } else {
            props.router?.navigate(`/`)
        }
    })
}

export default withRouter(Base);