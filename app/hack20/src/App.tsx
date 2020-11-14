import React from 'react';
import './App.css';
import { Button, Container, Divider, Grid, Header, Icon, Menu, Segment } from 'semantic-ui-react';
import AceEditor from 'react-ace';
import Listen from './components/Listen';

const onChange = (newValue: string) => {
  console.log("change", newValue);
}

const App = () => {
  return (
    <div>
      <div>
        <Menu><Menu.Item name='app'>My App</Menu.Item></Menu>
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
