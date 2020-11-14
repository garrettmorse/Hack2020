import React from 'react';

class Output extends React.Component<any, any> {
    constructor(props: any) {
        super(props);
        this.state = {
            output: 'Hello, World!'
        }
    }

    render() {
        return (
            <p>{this.state.output}</p>
        );
    }
}

export default Output;