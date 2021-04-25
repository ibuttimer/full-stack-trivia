import React, { useState, useEffect, useRef } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import $ from 'jquery';

import '../stylesheets/AddQuestionView.css';


function AddQuestionView () {

    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [difficulty, setDifficulty] = useState(1);
    const [category, setCategory] = useState(1);
    const [categories, setCategories] = useState({});

    const questionForm = useRef(null);

    useEffect(() => {
        $.ajax({
          url: `/api/categories?pagination=n&type=map`,
          type: "GET",
          success: (result) => {
            setCategories(result.categories)
            setCategory(
                Math.min(...Object.keys(result.categories).map(id=>parseInt(id)))
            )
            return;
          },
          error: (error) => {
            alert('Unable to load categories. Please try your request again')
            return;
          }
        })
    }, []); // https://www.robinwieruch.de/react-useeffect-hook mount


    function submitQuestion(event) {
        event.preventDefault();
        $.ajax({
            url: '/api/questions',
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify({
                question: question,
                answer: answer,
                difficulty: difficulty,
                category: category
            }),
            xhrFields: {
                withCredentials: true
            },
            crossDomain: true,
            success: (result) => {

                setQuestion("");
                setAnswer("");
                setDifficulty(1);
                setCategory(1);

                questionForm.current.reset();
                return;
            },
            error: (error) => {
                var msg = 'Unable to add question. Please try your request again.';
                if (error.responseJSON.detailed_message) {
                    msg += '\nReason: ' + error.responseJSON.detailed_message
                }
                alert(msg)
                return;
            }
        })
    }

    function handleChange(event) {
        switch (event.target.name) {
            case "question":    setQuestion(event.target.value);    break;
            case "answer":      setAnswer(event.target.value);      break;
            case "difficulty":  setDifficulty(event.target.value);  break;
            case "category":    setCategory(event.target.value);    break;
            default:                                                break;
        }
    }

    function validateForm() {
        return question.length > 0 && answer.length > 0;
    }

    return (
           <div id="add-form">
             <h2>Add a New Trivia Question</h2>

             <Form id="add-question-form" ref={questionForm} onSubmit={submitQuestion}>
                 <Form.Group size="lg" controlId="question">
                   <Form.Label>Question</Form.Label>
                   <Form.Control
                     autoFocus
                     name="question"
                     type="text"
                     value={question}
                     onChange={handleChange}
                   />
                 </Form.Group>
                 <Form.Group size="lg" controlId="answer">
                   <Form.Label>Answer</Form.Label>
                   <Form.Control
                     name="answer"
                     type="text"
                     value={answer}
                     onChange={handleChange}
                   />
                 </Form.Group>

                 <Form.Row>
                     <Form.Group as={Col} size="lg" controlId="difficulty">
                       <Form.Label>Difficulty</Form.Label>
                       <Form.Control
                         as="select"
                         name="difficulty"
                         value={difficulty}
                         onChange={handleChange}>
                             <option>1</option>
                             <option>2</option>
                             <option>3</option>
                             <option>4</option>
                             <option>5</option>
                       </Form.Control>
                     </Form.Group>

                     <Form.Group as={Col} size="lg" controlId="category">
                       <Form.Label>Category</Form.Label>
                       <Form.Control
                         as="select"
                         name="category"
                         value={category}
                         onChange={handleChange}>
                           {Object.keys(categories).map(id => {
                               return (
                                 <option key={id} value={id}>{categories[id]}</option>
                               )
                             })}
                       </Form.Control>
                     </Form.Group>
                 </Form.Row>
                 <Form.Group as={Row}>
                     <Col sm={{ span: 10, offset: 5 }}>
                         <Button block size="lg" className="col-sm-2" type="submit" disabled={!validateForm()}>
                           Submit
                         </Button>
                     </Col>
                   </Form.Group>
             </Form>
           </div>
        );
}

export default AddQuestionView;
