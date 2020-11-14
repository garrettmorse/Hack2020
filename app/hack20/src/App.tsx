import React from 'react';
import './App.css';
import { Button, Container, Divider, Grid, Header, Icon, Menu, Segment } from 'semantic-ui-react';
import AceEditor from 'react-ace';
import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/ext-language_tools"
import Listen from './components/Listen';

const onChange = (newValue: string) => {
  console.log("change", newValue);
}

const App = () => {
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
                <Listen />
              </Grid.Column>

              <Grid.Column>
                <Header as='h3'>Code</Header>
                <Button icon labelPosition='left' >
                  <Icon name='play' />
                  Run
                  </Button>
                <AceEditor
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

export default App;
