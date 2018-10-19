import React, { Component } from "react";
import { Row, Col, Button } from "reactstrap";
import PropTypes from "prop-types";

export default class GetOddsAndBalanceComponent extends Component {
    render() {
        const {
            blue,
            red,
            loadingOdds,
            onGetBalance,
            loadingBalance,
            loadingBalanceError
        } = this.props;
        const loadingRow = loadingOdds ? (
            <Row key="loadingodds">
                <h2>Loading odds</h2>
            </Row>
        ) : null;
        const oddsRow = !loadingOdds ? (
            <Row key="odds">
                <Col />
                <Col>
                    <h2>{blue.toPrecision(2)}</h2>
                </Col>
                <Col>
                    <h2>-</h2>
                </Col>
                <Col>
                    <h2>{red.toPrecision(2)}</h2>
                </Col>
                <Col />
            </Row>
        ) : null;
        return [
            loadingRow,
            oddsRow,
            <Row key="balance">
                <Col>
                    <Button
                        onClick={onGetBalance}
                        disabled={loadingBalance}
                        color={loadingBalanceError ? "danger" : "secondary"}
                    >
                        {loadingBalance ? "..." : "Balance Teams → "}
                    </Button>
                </Col>
            </Row>
        ];
    }
}

GetOddsAndBalanceComponent.propTypes = {
    blue: PropTypes.number,
    red: PropTypes.number,
    onGetBalance: PropTypes.func,
    loadingOdds: PropTypes.bool,
    loadingOddsError: PropTypes.string,
    loadingBalanceError: PropTypes.string,
    loadingBalance: PropTypes.bool
};
