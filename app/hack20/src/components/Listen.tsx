import React from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { Button, Container } from 'semantic-ui-react';

const Listen = () => {
    const { transcript, resetTranscript } = useSpeechRecognition();

    function hello() {
        return 'nope';
    }
    return (
        <Container>
            <Button onClick={() => SpeechRecognition.startListening()}>Record</Button>
            <Button onClick={SpeechRecognition.stopListening}>Send</Button>
            <Button onClick={resetTranscript}>Clear</Button>
            <Container>
                <p>{transcript}</p>
            </Container>
        </Container>
    )
}

export default Listen