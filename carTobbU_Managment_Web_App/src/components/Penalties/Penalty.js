
import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";

import {
    Button,
    Card,
    Image,
    Placeholder,
    Modal,
    Icon,
    Input,
    Label
} from "semantic-ui-react";

/* Form class component */
class Penalty extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    componentDidMount() {
    }

    render() {
        const {
            penalty
        } = this.props;

        // const { loading } = this.state;

        /* Renders form component */
        return (
            <>
                <Card key={penalty.type}>
                    <Image
                        style={{ width: "290px", height: "193px" }}
                        src={penalty.image}
                    />
                    <Card.Content>
                        <>
                            <Card.Header>{penalty.type}</Card.Header>
                            <Card.Meta>{`Report Time: ${penalty.time}`}</Card.Meta>
                            <Card.Description>
                                <Card.Content description={"Note: " + penalty.notes} />
                                <Card.Content description={"Car Plate: " + penalty.carPlate} />
                                <Label color="orange">
                                    <Icon name="hand paper" />
                                    {penalty.date}
                                </Label>
                            </Card.Description>
                        </>
                    </Card.Content>
                </Card>
            </>
        );
    }
}

export default Penalty;