import React from 'react';
import { Button, Container, Icon } from 'semantic-ui-react';
import AceEditor from 'react-ace';
import 'ace-builds/src-min-noconflict/mode-python';
import 'ace-builds/src-min-noconflict/theme-github';


class MyEditor extends React.Component<any, any> {
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
                    value={this.props.code}
                    style={{ marginTop: 5 }}
                    mode='python'
                    onChange={this.props.onCodeChange}
                    editorProps={{ $blockScrolling: true }}
                    width='100%'
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


export default MyEditor