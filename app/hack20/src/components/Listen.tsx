import React from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { Button, Container, Icon } from 'semantic-ui-react';

const Listen = (props: any) => {
    const { transcript, resetTranscript } = useSpeechRecognition();

    return (
        <Container>
            <Button onClick={() => SpeechRecognition.startListening()}>Record</Button>
            <Button onClick={() => {
                resetTranscript();
                props.onTextChange(transcript);
            }
            }>Clear</Button>
            <Button onClick={() => {
                props.onTextChange(transcript);
                props.handleRecording();
            }
            }>Send </Button>
            {props.loading ? <Icon style={{ marginLeft: 10 }} loading name='sync' /> : ''}
            <p>{transcript}</p>
        </Container>
    )
}

export default Listen