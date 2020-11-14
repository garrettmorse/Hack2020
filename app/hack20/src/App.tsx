import React from 'react';
import './App.css';
import { Container, Divider, Grid, Header, Icon, Menu, Segment } from 'semantic-ui-react';
import MyEditor from './components/Editor';
import Listen from './components/Listen';
import AppRoutes from './service/app-routes';
import { sample } from './static/constants.json';

class App extends React.Component<{}, { transcript: string, code: string, output: string }> {
  constructor(props: any) {
    super(props);
    this.sendRecording = this.sendRecording.bind(this);
    this.onTextChange = this.onTextChange.bind(this);
    this.onOutputChange = this.onOutputChange.bind(this)
    this.state = {
      transcript: '',
      code: sample,
      output: ''
    }
  }
  sendRecording() {
    const data = JSON.stringify({ transcript: this.state.transcript, code: this.state.code });
    // console.log(`data being sent: ${data}`);
    AppRoutes.sendText(data)
      .then(res => {
        this.onCodeChange(res.data);
      })
      .catch(e => {
        console.log(e);
        alert(e);
      })
  }

  execCode() {
    const data = JSON.stringify(this.state.code);
    AppRoutes.sendText(data)
      .then(res => {
        this.onOutputChange(res.data);
      })
      .catch(e => {
        console.log(e);
        alert(e);
      })
  }

  onTextChange(newText: string) {
    this.setState({ ...this.state, transcript: newText });
    // console.log(`update state.transcript: ${this.state.transcript}`);
  }

  onCodeChange(newCode: string) {
    this.setState({ ...this.state, code: newCode });
    // console.log(`update state.code: ${this.state.code}`);
  }

  onOutputChange(newOutput: string) {
    this.setState({ ...this.state, output: newOutput });
    // console.log(`update state.output: ${this.state.output}`);
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
                  <Listen onTextChange={this.onTextChange} text={this.state.transcript} handleRecording={this.sendRecording.bind(this)} />
                </Grid.Column>

                <Grid.Column>
                  <Header as='h3'>Code</Header>
                  <MyEditor onCodeChange={this.onCodeChange.bind(this)} code={this.state.code} />
                </Grid.Column>
              </Grid>

              <Divider vertical><Icon name='long arrow alternate right' /></Divider>
            </Segment>
            <Container>
              <Header as='h3'>Output</Header>
              <p>Hello, World!</p>
            </Container>
          </Segment>
        </div>
      </div >
    );
  }
}

export default App;
