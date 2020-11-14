import React from 'react';
import './App.css';
import { Container, Divider, Grid, Header, Menu, Segment } from 'semantic-ui-react';
import Editor from './components/Editor';
import Listen from './components/Listen';
import AppRoutes from './service/app-routes';

class App extends React.Component<{}, { transcript: string, code: string, sample: string }> {
  constructor(props: any) {
    super(props);
    this.sendRecording = this.sendRecording.bind(this);
    this.onTextChange = this.onTextChange.bind(this);
    this.state = {
      transcript: '',
      code: '',
      sample: "import os\nimport sys\n\n# Start talking to get started!\n#\n# If nothing comes to mind, here's a good example to get started...\n#   define a function helloworld that takes no arguments\n#   print helloworld\n"
    }
  }
  sendRecording() {
    AppRoutes.sendText(this.state.transcript)
      .then(res => {
        console.log(res);
        alert(res);
      })
      .catch(e => {
        console.log(e);
        alert(e);
      })
  }

  onTextChange(newText: string) {
    this.setState({ ...this.state, transcript: newText });
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
                  <Editor text={this.state.sample} />
                </Grid.Column>
              </Grid>

              <Divider vertical>==&gt;</Divider>
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
