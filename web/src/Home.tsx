import React from "react";
import {Button, Col, Form, Input, Row} from "antd";

class Home extends React.Component<any, any> {

    render() {
        return (
            <>
                <Row justify="center">
                    <Col xs={24} sm={12} md={12} lg={8}>
                        <Form
                            name="basic"
                            initialValues={{ remember: true }}
                            style={{
                                backgroundColor: "white",
                                padding: "25px 20px 5px 20px",
                                borderRadius: "5pt"
                            }}
                        >
                            <Form.Item
                                label="Имя"
                                name="name"
                                rules={[{required: true, message: "введите имя"}]}
                            >
                                <Input />
                            </Form.Item>
                            <Form.Item
                                label="Код игры"
                                name="code"
                                rules={[{required: true, message:"введите код"}]}
                            >
                                <Input />
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit">
                                    Присоединиться
                                </Button>
                            </Form.Item>
                        </Form>
                    </Col>
                </Row>
            </>
        );
    }

}

export default Home;