import React from 'react';
import './App.css';
import { Container, Divider, Grid, Header, Icon, Menu, Segment } from 'semantic-ui-react';
import MyEditor from './components/Editor';
import Listen from './components/Listen';
import Output from './components/Output';
import AppRoutes from './service/app-routes';
import { sample } from './static/constants.json';

class App extends React.Component<{}, { execLoader: boolean, sendLoader: boolean, transcript: string, code: string, output: string }> {
  constructor(props: any) {
    super(props);
    this.state = {
      execLoader: false,
      sendLoader: false,
      transcript: '',
      code: sample,
      output: ''
    }
  }
  sendRecording = (finalScript: string) => {
    const data = JSON.stringify({ transcript: finalScript, code: this.state.code });
    console.log(`recording being sent: ${data}`);
    this.setState({ sendLoader: true });
    AppRoutes.sendText(data)
      .then(res => {
        this.onCodeChange(res.data);
        this.setState({ sendLoader: false });
      })
      .catch(e => {
        console.log(e);
        alert(e);
      })
  }

  execCode = () => {
    const data = JSON.stringify({ code: this.state.code });
    console.log(`code being sent: ${data}`);
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

  onCodeChange = (newCode: string) => {
    this.setState({ code: newCode });
    // console.log(`update state.code: ${ this.state.code }`);
  }

  onOutputChange = (newOutput: string) => {
    this.setState({ output: newOutput });
    console.log(`update state.output: ${this.state.output}`);
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
        <div>
          <Segment>
            <Segment>
              <Grid columns={2} >
                <Grid.Column>
                  <Header as='h3'>Code</Header>
                  <MyEditor loading={this.state.execLoader}
                    handleCode={this.execCode.bind(this)}
                    onCodeChange={this.onCodeChange.bind(this)}
                    code={this.state.code} />
                </Grid.Column>
                <Grid.Column>
                  <Header as='h3'>Output</Header>
                  <span style={{ whiteSpace: 'pre-line' }}>{this.state.output}</span>
                  {/* <Output output={this.state.output} /> */}
                </Grid.Column>


              </Grid>

              <Divider vertical><Icon name='long arrow alternate right' /></Divider>
            </Segment>
            <Container active>

              <Header as='h3'>Record Speech</Header>
              <Listen executeCode={this.execCode}
                loading={this.state.sendLoader}
                onTextChange={this.onTextChange}
                text={this.state.transcript}
                handleRecording={this.sendRecording.bind(this)} />
            </Container>
          </Segment>
        </div>
      </div >
    );
  }
}

export default App;
