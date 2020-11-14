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
    this.sendRecording = this.sendRecording.bind(this);
    this.onTextChange = this.onTextChange.bind(this);
    this.onOutputChange = this.onOutputChange.bind(this)
    this.state = {
      execLoader: false,
      sendLoader: false,
      transcript: '',
      code: sample,
      output: ''
    }
  }
  sendRecording() {
    const data = JSON.stringify({ transcript: this.state.transcript, code: this.state.code });
    // console.log(`recording being sent: ${data}`);
    this.setState({ ...this.state, sendLoader: true });
    AppRoutes.sendText(data)
      .then(res => {
        this.onCodeChange(res.data);
        this.setState({ ...this.state, sendLoader: false });
      })
      .catch(e => {
        console.log(e);
        alert(e);
      })
  }

  execCode() {
    const data = JSON.stringify(this.state.code);
    console.log(`code being sent: ${data}`);
    this.setState({ ...this.state, execLoader: true });
    AppRoutes.sendText(data)
      .then(async res => {
        await this.sleep(2000);
        this.onOutputChange(res.data);
        this.setState({ ...this.state, execLoader: false });
      })
      .catch(e => {
        console.log(e);
        alert(e);
      })
  }

  onTextChange(newText: string) {
    this.setState({ ...this.state, transcript: newText });
    // console.log(`update state.transcript: ${ this.state.transcript }`);
  }

  onCodeChange(newCode: string) {
    this.setState({ ...this.state, code: newCode });
    // console.log(`update state.code: ${ this.state.code }`);
  }

  onOutputChange(newOutput: string) {
    this.setState({ ...this.state, output: newOutput });
    // console.log(`update state.output: ${ this.state.output }`);
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
                  <Header as='h3'>Record Speech</Header>
                  <Listen loading={this.state.sendLoader}
                    onTextChange={this.onTextChange}
                    text={this.state.transcript}
                    handleRecording={this.sendRecording.bind(this)} />
                </Grid.Column>

                <Grid.Column>
                  <Header as='h3'>Code</Header>
                  <MyEditor loading={this.state.execLoader}
                    handleCode={this.execCode.bind(this)}
                    onCodeChange={this.onCodeChange.bind(this)}
                    code={this.state.code} />
                </Grid.Column>
              </Grid>

              <Divider vertical><Icon name='long arrow alternate right' /></Divider>
            </Segment>
            <Container active>
              <Header as='h3'>Output</Header>
              <Output output={this.state.output} />
            </Container>
          </Segment>
        </div>
      </div >
    );
  }
}

export default App;
