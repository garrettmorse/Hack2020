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
                <Button
                    color="green"
                    onClick={this.props.handleCode}
                    icon labelPosition='left' >
                    <Icon name='play' />
                    Run
                </Button>
                <Button
                    onClick={this.props.handleUndo}
                    icon labelPosition='left' >
                    <Icon name='redo' />
                    Undo
                </Button>
                {this.props.loading ? <Icon style={{ marginLeft: 10 }} loading name='sync' /> : ''}
                <AceEditor
                    value={this.props.code}
                    style={{ marginTop: 5 }}
                    mode='python'
                    onChange={this.props.onCodeChange}
                    editorProps={{ $blockScrolling: true }}
                    width='100%'
                    height='80vh'
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