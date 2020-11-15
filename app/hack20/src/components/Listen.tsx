import React, { useState, useEffect } from 'react';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { Button, Container, Header, Segment, Portal } from 'semantic-ui-react';
import Siriwave from 'react-siriwave';
import { async } from 'q';

const Listen = (props: any) => {
    const [showTranscript, setShowTranscript] = useState<boolean>(false);
    const [open, setOpen] = useState<boolean>(true); // for use with voice commands portal
    useEffect(() => {
        SpeechRecognition.startListening({ continuous: true });
    }, []);
    const commands = [
        {
            command: '*start recording',
            callback: async () => {
                resetTranscript();
                setShowTranscript(true);
            }
        },
        {
            command: '*send message',
            callback: async () => {
                if (showTranscript) {
                    setShowTranscript(false);
                    let finalStr = finalTranscript.replace('send message', '');
                    await props.handleRecording(finalStr);
                    console.log(finalStr);
                    await SpeechRecognition.startListening({ continuous: true });
                    resetTranscript();
                }
            }
        },
        {
            command: '*execute code',
            callback: async () => {
                if (!showTranscript) {
                    await props.executeCode();
                    console.log('code executed');
                    resetTranscript();
                }
            }
        },
        {
            command: '*clear recording',
            callback: async () => {
                resetTranscript();
                console.log('cleared transcript');
            }
        },
        {
            command: '*stop recording',
            callback: async () => {
                setShowTranscript(false);
                resetTranscript();

                console.log('stopped listening');
            }
        },
        {
            command: '*undo code',
            callback: async () => {
                if (!showTranscript) {
                    await props.handleUndo();
                }
            }
        },
        {
            command: '*voice commands',
            callback: async () => {
                setOpen(!open);
            }
        },
        {
            command: '*clear output',
            callback: async () => {
                props.handleOutputClear();
            }
        }
    ]

    const { transcript, finalTranscript, resetTranscript } = useSpeechRecognition({ commands });
    const handleOpen = () => {
        setOpen(true);
    }

    const handleClose = () => {
        setOpen(false);
    }
    // const buttonOffset = showTranscript ? 73 : 90;
    const toggleOpacity = showTranscript ? 0.4 : 1;
    const clearOutputOffset = showTranscript ? 218 : 92;
    const voiceCommandsOffset = showTranscript ? 374 : 248;
    return (
        <div>
            <Header as='h3'>Record Speech</Header>

            <Container>
                <Portal
                    open={open}
                >
                    <Segment
                        style={{
                            right: '1%',
                            position: 'fixed',
                            top: '5%',
                            zIndex: 1000,
                            opacity: toggleOpacity
                        }}
                    >
                        {/* To start recording, say 'Start Recording'. To send your message, say 'Send Message'. To clear the transcript, say 'Clear Recording'. To toggle this menu, say 'Voice Commands'. To stop the recording, say 'Stop Recording'. To execute code, say 'Execute Code'. To undo code, say 'Undo Code'. */}
                        <Header>Voice Commands</Header>
                        <p><strong>While Recording</strong></p>
                        <ul>
                            <li>Send Message</li>
                            <li>Stop Recording</li>
                        </ul>
                        <p><strong>While Not Recording</strong></p>
                        <ul>
                            <li>Execute Code</li>
                            <li>Undo Code</li>
                            <li>Start Recording</li>
                        </ul>
                        <p><strong>At Any Time</strong></p>
                        <ul>
                            <li>Voice Commands</li>
                            <li>Clear Recording</li>
                            <li>Clear Output</li>
                        </ul>
                    </Segment>
                </Portal>
                <Button
                    style={{ position: 'fixed', top: 2, right: clearOutputOffset, cursor: 'pointer', zIndex: 1000 }}
                    onClick={async () => {
                        setOpen(!open);
                    }}>
                    Voice Commands
                </Button>
                <Button
                    style={{ position: 'fixed', top: 2, right: voiceCommandsOffset, cursor: 'pointer', zIndex: 1000 }}
                    onClick={async () => {
                        props.handleOutputClear();
                    }}>
                    Clear Output
                </Button>
                {showTranscript ?
                    (<Button.Group>
                        <Button
                            style={{ position: 'fixed', top: 2, right: 74, cursor: 'pointer', zIndex: 1000 }}
                            color='yellow'
                            onClick={async () => {
                                resetTranscript();
                            }}>
                            Clear Recording
                    </Button>
                        <Button
                            style={{ position: 'fixed', top: 2, right: 3, cursor: 'pointer', zIndex: 1000 }}
                            color='red'
                            onClick={async () => {
                                resetTranscript();
                                setShowTranscript(false);
                            }}>
                            Stop
                    </Button>

                    </Button.Group>) :

                    (<Button
                        style={{ color: 'whitesmoke', backgroundColor: '#6868f6', position: 'fixed', top: 2, right: 0, cursor: 'pointer', zIndex: 1000 }}

                        onClick={async () => {
                            resetTranscript();
                            setShowTranscript(true);
                        }}>
                        Record
                    </Button>)}

                <div style={{ background: 'white' }}>
                    {showTranscript ? (<Siriwave cover={true} amplitude={showTranscript ? 1 : 0.01} style='ios9' />) : null}
                </div>
                <p>{showTranscript ? transcript : ''}</p>
            </Container >
        </div>
    )
}

export default Listen