import Title from "antd/es/typography/Title";
import {List} from "antd";
import React from "react";

export default class PlayersList extends React.Component<{ players: string[] }, {}> {
    render() {
        return (
            <>
                <Title level={4}>Участники</Title>
                <List
                    style={{marginTop: "20pt", borderRadius: "3pt", backgroundColor: "white"}}
                    bordered
                    size="large"
                    dataSource={this.props.players}
                    renderItem={item => (
                        <List.Item>{item}</List.Item>
                    )}
                />
            </>
        );
    }
}