import React from "react";
import {Button, Col, Form, Input, message, Row} from "antd";
import {join} from "./api";
import withRouter from "./withRouter";

class Home extends React.Component<any, any> {

    render() {
        return (
            <>
                <Row justify="center">
                    <Col xs={24} sm={12} md={12} lg={8}>
                        {this.joinForm()}
                    </Col>
                </Row>
            </>
        );
    }

    joinForm() {
        return (
            <Form
                name="basic"
                initialValues={{ remember: true }}
                style={{
                    backgroundColor: "white",
                    padding: "25px 20px 5px 20px",
                    borderRadius: "5pt"
                }}
                onSubmitCapture={() => {this.joinAction()}}
            >
                <Form.Item
                    label="Имя"
                    name="name"
                    rules={[{required: true, message: "введите имя"}]}
                >
                    <Input onChange={(e) => {this.setState({name: e.target.value})}} />
                </Form.Item>
                <Form.Item
                    label="Код игры"
                    name="code"
                    rules={[{required: true, message:"введите код"}]}
                >
                    <Input onChange={(e) => {this.setState({code: e.target.value})}} />
                </Form.Item>
                <Form.Item>
                    <Button
                        type="primary"
                        htmlType="submit"
                    >
                        Присоединиться
                    </Button>
                </Form.Item>
            </Form>
        );
    }

    joinAction() {
        join(this.state.name, this.state.code).then((result) => {
            if (result.ok) {
                console.log(result.value)
                this.props.router.navigate(`/game/${result.value}`)
            } else {
                message.error(`${result.error}`)
            }
        })
    }

}

export default withRouter(Home);