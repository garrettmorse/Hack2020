import React from 'react';
import { Button, Container, Icon } from 'semantic-ui-react';
import AceEditor from 'react-ace';
import 'brace/mode/python';

const onChange = (newValue: string) => {
    console.log(newValue);
}

class Editor extends React.Component<{ text: string }, { text: string }>{
    constructor(props: any) {
        super(props);
        this.state = {
            text: props.text
        };
    }
    componentDidMount() {
        const reactAceComponent = this.refs.reactAceComponent;
        console.log(reactAceComponent);
    }

    render() {
        return (
            <Container>
                <Button icon labelPosition='left' >
                    <Icon name='play' />
    Run
    </Button>
                <AceEditor
                    value={this.state.text}
                    style={{ marginTop: 5 }}
                    mode='python'
                    onChange={onChange}
                    editorProps={{ $blockScrolling: true }}
                    setOptions={{
                        enableBasicAutocompletion: true,
                        enableLiveAutocompletion: true,
                        enableSnippets: true
                    }}
                />
            </Container >
        );
    }
}


export default Editor