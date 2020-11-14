import React from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { Button, Container } from 'semantic-ui-react';

const Listen = (props: any) => {
    const { transcript, resetTranscript } = useSpeechRecognition();

    return (
        <Container>
            <Button onClick={() => SpeechRecognition.startListening()}>Record</Button>
            <Button onClick={() => {
                props.onTextChange(transcript);
                props.handleRecording();
            }
            }>Send</Button>
            <Button onClick={() => {
                resetTranscript();
                props.onTextChange(transcript);
            }
            }>Clear</Button>
            <p>{transcript}</p>
        </Container>
    )
}

export default Listen