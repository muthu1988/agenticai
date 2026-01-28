import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import axios from 'axios'

// 1. Mistake: Missing type definitions for props in a TSX file
export default function UserProfile(props) {
  const router = useRouter()
  
  // 2. Mistake: Initializing state with wrong type (should be null or object)
  const [data, setData] = useState("");
  const [loading, setLoading] = useState(false);

  // 3. Mistake: useEffect missing dependency array (infinite loop)
  // 4. Mistake: Using a hardcoded URL instead of env variables
  useEffect(() => {
    setLoading(true);
    axios.get('http://localhost:3000/api/user?id=' + props.id)
      .then(res => {
        setData(res.data);
        setLoading(false);
      });
  }); 

  // 5. Mistake: Direct DOM manipulation in React
  const changeColor = () => {
    document.getElementById('title').style.color = 'red';
  }

  // 6. Mistake: Inline styles as strings (React requires objects)
  // 7. Mistake: Using <a> instead of Next.js <Link> for internal routing
  // 8. Mistake: No error handling for the 'data' object (will crash on data.name)
  return (
    <div style="padding: 20px; background: white;">
      <h1 id="title">User: {data.name}</h1>
      <p>Email: {data.info.email}</p>
      
      <button onClick={changeColor()}>
        Click me
      </button>

      <div className="links">
        <a href="/dashboard">Go to Dashboard</a>
      </div>

      {/* 9. Mistake: Mapping without a unique 'key' prop */}
      <ul>
        {data.posts.map(post => (
          <li>{post.title}</li>
        ))}
      </ul>

      {/* 10. Mistake: Using unoptimized <img> tag instead of next/image */}
      <img src={data.avatar} />
    </div>
  )
}
