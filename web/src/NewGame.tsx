import React from "react";
import Title from "antd/es/typography/Title";
import {Button, Col, Form, List, message, Row, Space} from "antd";
import Text from "antd/es/typography/Text";
import {green} from "@ant-design/colors";
import { CopyOutlined } from '@ant-design/icons';

export interface NewGameParameters {
    code: string;
    players: string[];
}

const newGame0: NewGameParameters = {
    code: 'A657OTB4AT',
    players: [
        'One',
        'Two',
        'Three',
        'Four',
        'Five',
        'Six',
        'Seven'
    ]
};

class NewGame extends React.Component<any, NewGameParameters> {
    constructor(props: any) {
        super(props);
        this.state = {
            code: '',
            players: [] as string[]
        }
    }

    componentDidMount() {
        this.setState(newGame0);
    }

    render() {
        return (
            <>
                <Row justify="center">
                    <Col xs={24} sm={24} md={24} lg={7} style={{paddingTop: "25px"}}>
                        <Title>Новая игра</Title>
                        <Text
                            style={{
                                backgroundColor: green[2],
                                fontSize: "2rem",
                                padding: "10px",
                                borderRadius: "3pt",
                                cursor: "pointer"
                            }}
                            onClick={() => {
                                navigator.clipboard.writeText(this.state.code);
                                message.success('Copied!');
                            }}
                        >
                            {this.state.code} <CopyOutlined />
                        </Text>
                    </Col>
                    <Col xs={24} sm={24} md={24} lg={10} style={{paddingTop: "35px"}}>
                        <Title level={4}>
                            Участники
                        </Title>
                        <List
                            style={{marginTop: "20pt", borderRadius: "3pt", paddingTop: "10pt", backgroundColor: "white"}}
                            bordered
                            size="large"
                            dataSource={this.state.players}
                            renderItem={item => (
                                <List.Item>
                                    {item}
                                </List.Item>
                            )}
                        />
                        <Row justify="center">
                            <Form style={{paddingTop:"25pt"}}>
                                <Space size="large">
                                    <Button type="primary" danger={true}>✗&nbsp;&nbsp;&nbsp;Завершить</Button>
                                    <Button type="primary">Начать&nbsp;&nbsp;&nbsp;→</Button>
                                </Space>
                            </Form>
                        </Row>
                    </Col>
                </Row>
            </>
        );
    }

}

export default NewGame;