import React from "react";
import withRouter, {RouterProps} from "./withRouter";
import Title from "antd/es/typography/Title";
import {Button, Col, message, Row, Space} from "antd";
import PlayersList from "./PlayersList";
import Action from "./Action";
import {green, geekblue} from "@ant-design/colors";
import {load} from "./api";
import {CopyOutlined} from "@ant-design/icons";

export interface GameState {
    code: string;
    is_started: boolean;
    is_spectator: boolean;
    correct_sequence?: string;
    actual_sequence?: string;
    players: string[];
    player_numbers?: string[];
}

class Game extends React.Component<RouterProps, GameState> {
    constructor(props: RouterProps) {
        super(props);
        this.state = {
            code: '',
            players: [],
            is_spectator: false,
            is_started: false
        };
    }

    componentDidMount() {
        load(this.props.router?.params.id).then((result) => {
            if (result.ok) {
                this.setState(result.value);
            } else {
                this.props.router?.navigate('/');
            }
        })
    }

    render() {
        if (this.state.is_started) {
            return this.began();
        } else {
            return this.newGame();
        }
    }

    newGame() {
        return (
            <>
                <Row justify="center">
                    <Col xs={24} sm={24} md={24} lg={7} style={{paddingTop: "25px"}}>
                        <Title>Новая игра</Title>
                        <Action
                            action={() => {
                                navigator.clipboard.writeText(this.state.code);
                                message.success('Copied!');
                            }}>
                            {this.state.code} <CopyOutlined />
                        </Action>
                    </Col>
                    <Col xs={24} sm={24} md={24} lg={10} style={{paddingTop: "35px"}}>
                        <PlayersList players={this.state.players} />
                        <Row justify="center" style={{paddingTop:"25pt"}}>
                            {this.newGameControls()}
                        </Row>
                    </Col>
                </Row>
            </>
        );
    }

    newGameControls() {
        return (
            <Space size="large">
                <Button
                    type="primary"
                    danger={true}
                    onClick={() => this.props.router?.navigate('/')}
                >
                    ✗&nbsp;&nbsp;&nbsp;Завершить
                </Button>
                <Button
                    type="primary"
                    onClick={() => this.props.router?.navigate(`/game/${this.state.code}`)}
                >
                    Начать&nbsp;&nbsp;&nbsp;→
                </Button>
            </Space>
        );
    }

    began() {
        return (
            <>
                <Row justify="center">
                    <Col xs={24} sm={24} md={24} lg={7} style={{paddingTop: "25px"}}>
                        {this.info()}
                    </Col>
                    <Col xs={24} sm={24} md={24} lg={10} style={{paddingTop: "35px"}}>
                        <PlayersList players={this.state.players} />
                        <Row justify="center" style={{paddingTop:"25pt"}}>
                            {this.controls()}
                        </Row>
                    </Col>
                </Row>
            </>
        );
    }

    info() {
        if (this.state.is_spectator) {
            return (
                <>
                    {this.expected()}
                    {this.actual()}
                </>
            );
        }
        return this.numbers()
    }

    numbers() {
        if (!this.state.player_numbers) {
            return <></>
        }
        return (
            <>
                <Title>Твои числа</Title>
                <Space>
                    {
                        this.state.player_numbers.map((number) => {
                            return (
                                <Action action={() => {}}>{number}</Action>
                            );})
                    }
                </Space>
            </>
        );
    }

    expected() {
        if (!this.state.correct_sequence) {
            return <></>
        }
        return (
            <>
                <Title level={2}>Ожидается</Title>
                <Title style={{color: green[6]}}>{this.state.correct_sequence}</Title>
            </>
        );
    }

    actual() {
        if (!this.state.actual_sequence) {
            return <></>
        }
        return (
            <>
                <Title level={2}>Собрано</Title>
                <Title style={{color: geekblue[6]}}>{this.state.actual_sequence}</Title>
            </>
        );
    }

    controls() {
        if (!this.state.is_spectator) {
            return <></>
        }
        return (
            <Space size="large">
                <Button type="primary" onClick={() => {}}>
                    ✱&nbsp;&nbsp;&nbsp;Перезапустить
                </Button>
                <Button
                    type="primary"
                    danger={true}
                    onClick={() => {
                        this.props.router?.navigate('/')
                    }}
                >
                    ✗&nbsp;&nbsp;&nbsp;Завершить
                </Button>
            </Space>
        );
    }
}

export default withRouter(Game);