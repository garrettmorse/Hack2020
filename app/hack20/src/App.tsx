import React from 'react';
import './App.css';
import { Container, Divider, Grid, Header, Icon, Menu, Segment } from 'semantic-ui-react';
import MyEditor from './components/Editor';
import Listen from './components/Listen';
import Output from './components/Output';
import AppRoutes from './service/app-routes';
import { sample } from './static/constants.json';

class App extends React.Component<{}, { codeEdited: boolean, execLoader: boolean, sendLoader: boolean, transcript: string, code: string, output: string }> {
  constructor(props: any) {
    super(props);
    this.state = {
      execLoader: false,
      sendLoader: false,
      transcript: '',
      code: sample,
      codeEdited: false,
      output: ''
    }
  }
  /*
  * operations/process
  */
  sendRecording = (finalScript: string) => {
    const data = JSON.stringify({ transcript: finalScript, code: this.state.code, edited: this.state.codeEdited });
    console.log(data);
    this.setState({ sendLoader: true });
    AppRoutes.sendText(data)
      .then(res => {
        this.onCodeChange(res.data.code, false);
        this.setState({ sendLoader: false });
      })
      .catch(e => {
        console.log(e);
        alert(e);
      })
  }

  /*
  * operations/execute
  */
  execCode = () => {
    const data = JSON.stringify({ code: this.state.code });
    console.log(data);
    this.setState({ execLoader: true });
    AppRoutes.execCode(data)
      .then(async res => {
        // await this.sleep(2000);
        console.log(res);
        this.onOutputChange(res.data.output);
        this.setState({ execLoader: false });
      })
      .catch(e => {
        console.log(e);
        alert(e);
      })
  }

  onTextChange = (newText: string) => {
    this.setState({ transcript: newText });
    // console.log(`update state.transcript: ${ this.state.transcript }`);
  }

  onCodeChange = (newCode: string, codeEdited = true) => {
    this.setState({ code: newCode, codeEdited });
    console.log(`update state.code: ${this.state.code}`);
  }

  undoCode = async () => {
    await AppRoutes.undoCode()
      .then(res => {
        this.onCodeChange(res.data.code);
      });
  }

  onOutputChange = (newOutput: string) => {
    const outputStr = this.state.output === "" ? newOutput : this.state.output + '\n-----\n' + newOutput;
    console.log(`before update state.output: ${this.state.output}`);
    this.setState({ output: outputStr });
    console.log(`after update state.output: ${this.state.output}`);
  }

  onOutputClear = () => {
    this.setState({ output: '' });
  }
  sleep(ms: any) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  render() {
    return (
      <div>
        <div>
          <Menu><Menu.Item name='app'>Hack 2020</Menu.Item></Menu>
        </div>
        <div style={{ margin: 10 }}>
          <Grid style={{ borderRadius: 5 }} celled columns={2} >
            <Grid.Column style={{ height: '93.2vh' }}>
              <Header as='h3'>Code</Header>
              <MyEditor
                loading={this.state.execLoader}
                handleCode={this.execCode}
                onCodeChange={(newCode: string) => this.onCodeChange(newCode)}
                handleUndo={this.undoCode}
                code={this.state.code} />
            </Grid.Column>
            <Grid.Column>
              <Grid celled='internally'>
                <Grid.Row style={{ height: '50vh' }}>
                  <Container>
                    <Listen executeCode={this.execCode}
                      loading={this.state.sendLoader}
                      onTextChange={this.onTextChange}
                      onCodeChange={(newCode: string) => { this.onCodeChange(newCode, false) }}
                      text={this.state.transcript}
                      handleUndo={this.undoCode}
                      handleRecording={this.sendRecording}
                      handleOutputClear={this.onOutputClear}
                    />
                  </Container>
                </Grid.Row>
                <Grid.Row verticalAlign='bottom'>
                  <Container >
                    <Header style={{ marginTop: 10 }} as='h3'>Output</Header>
                    <span style={{ whiteSpace: 'pre-line' }}>{this.state.output}</span>
                    {/* <Output output={this.state.output} /> */}
                  </Container>
                </Grid.Row>
              </Grid>
            </Grid.Column>
          </Grid>

          <Divider hidden style={{ top: '67%' }} vertical>
            <Icon name='long arrow alternate right' />

          </Divider>
          <Divider hidden style={{ top: '33%' }} vertical><Icon name='long arrow alternate left' /></Divider>
        </div>
      </div >
    );
  }
}

export default App;
