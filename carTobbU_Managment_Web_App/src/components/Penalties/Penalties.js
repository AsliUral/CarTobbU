/* eslint-disable react/forbid-prop-types */
import _ from "lodash";
import React, { Component } from "react";
import { Card, Container } from "semantic-ui-react";
import PropTypes from "prop-types";
import Penalty from "../Penalties/Penalty.js"
import axios from "axios";
import { Header } from 'semantic-ui-react'


const styleLinkHref =
    "https://cdn.jsdelivr.net/npm/semantic-ui/dist/semantic.min.css";

/* Container of form components */
class Penalties extends Component {
    constructor(props) {
        super(props);
        const { penalties } = this.props;
        this.state = {
            penalties: []
        };
    }

    /* Loading animation with placeholders, lazy loading */
    componentDidMount() {
        axios.get(`http://smart-car-park-api.appspot.com/getPenalties`)
            .then(res => {
                const temp = res.data;
                var penalties = [];
                temp.forEach(function (data) {
                    if (data.type) {
                        if (!data.detectedStatus) {
                            penalties.push(data)
                        }
                    }
                });
                this.setState({ penalties });
            })
    }
    render() {
        const styleLink = document.createElement("link");
        styleLink.rel = "stylesheet";
        styleLink.href = styleLinkHref;
        document.head.appendChild(styleLink);

        // const { authorized, setAuthFalse, user } = this.props;
        const { penalties } = this.state;
        // const { jotformWidgets, setCurrentForm, selectedWidgets } = this.props;
        return (
            <>
                <Header as='h1' style={{ padding: "12px 12px 7px 12px", textAlign: "center" }}> Gelen Ceza Raporları</Header>
                <Container style={{ margin: 20 }}>
                    <>
                        <Card.Group doubling stackable style={{ position: "absolute", margin: "auto" }}>
                            {_.map(penalties, penalty => (
                                <Penalty
                                    key={penalty.id}
                                    penalty={penalty}
                                />
                            ))}
                        </Card.Group>
                    </>
                </Container>
            </>
        );
    }
}


export default Penalties;