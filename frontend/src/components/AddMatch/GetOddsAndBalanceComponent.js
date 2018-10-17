import React, { Component } from "react";
import { Row, Col, Button } from "reactstrap";

export default class GetOddsAndBalanceComponent extends Component {
    render() {
        return [
            <Row key="odds">
                <Col>
                    <h2>20</h2>
                </Col>
                <Col>
                    <h2>-</h2>
                </Col>
                <Col>
                    <h2>80</h2>
                </Col>
            </Row>,
            <Row key="balance">
                <Col>
                    <Button type="submit">Balance Teams → </Button>
                </Col>
            </Row>
        ];
    }
}
