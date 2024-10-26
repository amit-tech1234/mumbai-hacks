import { useState, useLayoutEffect, useEffect } from 'react'
import { useQuery, useMutation } from "react-query";
import { motion } from 'framer-motion'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { CardBody, CardContainer, CardItem } from "./components/ui/3d-card"
import { ChevronLeft, ArrowRightIcon } from 'lucide-react'
import { Player } from '@lottiefiles/react-lottie-player'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs"
import axios from 'axios'
import Chart from 'chart.js/auto'

const URL = 'https://ff68-61-246-51-230.ngrok-free.app/'

const uploadCSVFile = async (file) => {
  const formData = new FormData()
  formData.append("file", file)

  const response = await axios.post(URL, formData)

  return response.data
}

const UploadCardPage = () => {
  const [file, setFile] = useState('')

  const navigate = useNavigate()

  // React Query mutation for file upload
  const mutation = useMutation(uploadCSVFile, {
    onSuccess: (data) => {
      navigate(`/insights`, { state: data })
      localStorage.setItem('insights-data', JSON.stringify(data))
    },
    onError: (error) => {
      console.log(error)
    },
  });

  useEffect(() => {
    localStorage.setItem('insights-data', '')
  }, [])

  const handleFileChange = (e) => {
    e.preventDefault()

    const file = e.target.files?.[0]

    if (file) {
      setFile(file)

      mutation.mutate(e.target.files[0])
      event.target.value = ""
    }
  };

  return (
    <div className='main-app flex items-center justify-center min-h-screen bg-black'>
      <UploadCard 
        file={file}
        mutation={mutation} 
        handleFileChange={handleFileChange} 
      />
    </div>
  )
}

export default UploadCardPage

const UploadCard = ({ mutation, handleFileChange }) => {
  return (
      <motion.div
          className='relative flex flex-col gap-4 px-4'
          initial={{ opacity: 0.0, y: 150 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
              duration: 0.6,
              ease: 'easeIn'
          }}
      >
        <CardContainer className="inter-var">
          <CardBody className="bg-white/20 backdrop-blur-lg backdrop-filter relative group/card w-auto sm:w-[40rem] h-auto rounded-xl p-6">
            <CardItem 
              as='p' 
              translateZ="60"
              className="text-2xl w-full md:text-3xl font-bold text-white text-center"
            >
              <motion.span
                initial={{ opacity: 0.0, y: 150 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{
                    duration: 1,
                    delay: 0.6,
                    ease: 'easeInOut'
                }}
              >
                Discover Insights 
              </motion.span>
            </CardItem>
            <CardItem
              as="p"
              translateZ="30"
              className="font-thin text-white text-center mb-3 md:text-lg py-4"
            >
              <motion.span
                initial={{ opacity: 0.0, y: 150 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{
                    duration: 1,
                    delay: 0.7,
                    ease: 'easeInOut'
                }}
              >
                Depending on your uploaded data, we will suggest channel specific strategies that can boost
                engagment and retention.
              </motion.span>
            </CardItem>
            <motion.div 
              className="flex w-full justify-center items-center mt-5"
              initial={{ opacity: 0.0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{
                  duration: 1,
                  delay: 0.8,
                  ease: 'easeInOut'
              }}
            >
              <form className='w-full'>
                <input
                  id='file'
                  type="file"
                  accept=".csv"
                  onChange={handleFileChange}
                  disabled={mutation?.isLoading}
                  className="bg-black hidden" 
                />
                <CardItem
                  as='label'
                  htmlFor='file'
                  translateZ='100'
                  className='bg-black cursor-pointer hover:bg-gray-200 flex justify-center items-center gap-2 font-semibold capitalize bg-white rounded-xl w-full text-black px-7 py-4'
                >
                  <Player
                    loop
                    autoplay
                    src={'https://lottie.host/65cb0617-1124-4712-b0ce-b4b0ae1aa3a1/VvT3MCsBMA.json'}
                    style={{ height: '30px', width: '30px' }}
                  >
                  </Player>
                  <span className='text-xl'>
                    {mutation?.isError ? 'Oops! Let\'s try again' : mutation?.isLoading ? "Uploading..." : "Upload"}
                  </span>
                </CardItem>
              </form>
            </motion.div>
          </CardBody>
        </CardContainer>
      </motion.div>
  )
}

export const UserCardsPage = () => {
  const { state } = useLocation()

  return (
    <div className='main-app min-h-screen bg-black'>
      <UserCards data={state?.data} />
    </div>
  )
}

const UserCards = ({ data }) => {
  return (
    <div className='p-6 min-h-screen'>
      <Link to='/'>
        <button className='cursor-pointer transition duration-200 rounded-lg p-1 mb-4 bg-white hover:bg-gray-300'>
          <ChevronLeft />
        </button>
      </Link>

      <div>
        <h3 className='text-white font-semibold mb-2 text-3xl'>
          <motion.span
            initial={{ opacity: 0.0, y: 150 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{
                duration: 1,
                ease: 'easeInOut'
            }}
          >
            User Churn Overview
          </motion.span>
        </h3>
        <motion.span 
          className='text-white font-extralight'
          initial={{ opacity: 0.0, y: 150 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
              delay: 0.2,
              duration: 1,
              ease: 'easeInOut'
          }}
        >
          Analyzing User Feedback to Enhance Retention Strategies.
        </motion.span>
      </div>

      <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 mt-8'>
        {data?.map((userItem, idx) => (
          <UserCard idx={idx} {...userItem} {...userItem?.user_data} key={idx} />
        ))}
      </div>
    </div>
  )
}

const UserCard = (props) => {
  const {
    user_id,
    user_name, 
    location, 
    cultural_interests = [], 
    churn_reasons, 
    churn_status 
  } = props

  const churnTypes = {
    low: 'safe',
    medium: 'risk',
    high: 'churned'
  }

  const churnTypeLabels = {
    low: 'Safe',
    medium: 'At Risk',
    high: 'Churned'
  }

  const churnStatusType = churn_status?.risk?.toLowerCase()

  return (
    <Link to={`/${user_id}`} state={props}>
      <motion.div 
        className="user-card cursor-pointer bg-white/20 backdrop-blur-lg backdrop-filter rounded-lg p-3"
        initial={{ opacity: 0.0, y: 150 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
            duration: 1,
            delay: 0.1 * props?.idx,
            ease: 'easeInOut'
        }}
      >
        <div className="mb-2 flex justify-between items-center">
          <h5 className='font-bold mr-3 text-white'>{user_name || 'Amit Tiwari'}</h5>

          <div className={`churn churn--${churnTypes?.[churnStatusType]}`}>
            <div className='churn-status'>
            </div>
            <span>{churnTypeLabels?.[churnStatusType]}</span>
          </div>
        </div>

        <h5 className='text-white font-extralight mb-1 text-xs'>Location</h5>
        <p className="text-white text-sm font-light">{location}</p>

        <h5 className='text-white font-extralight mt-2 mb-1 text-xs'>Interests</h5>
        <p className="text-white text-sm font-light capitalize">
          {Array.isArray(cultural_interests) ? cultural_interests.join(', ') : cultural_interests}
        </p>

        <button className='user-card-button flex text-sm mt-3 text-white hover:text-gray-200 gap-1'>
          Get Insights <ArrowRightIcon className='user-card-arrow hover:text-gray-200' size={20} />
        </button>
      </motion.div>
    </Link>
  )
}

export const UserInsights = (props) => {
  const { state } = useLocation()

  const { user_name } = state

  const churnTypes = {
    low: 'safe',
    medium: 'risk',
    high: 'churned'
  }

  const churnTypeLabels = {
    low: 'Safe',
    medium: 'At Risk',
    high: 'Churned'
  }

  const strategyLabels = {
    sms: 'SMS',
    push_notifications: 'Push',
    email: 'Email',
    whatsapp: 'WhatsApp'
  }

  const churnStatusType = state?.churn_status?.risk?.toLowerCase()

  useLayoutEffect(() => {
    ;(async function() {
      new Chart(
        document.getElementById('historical-data').getContext('2d'),
        {
          type: 'doughnut',
          options: {  
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } }
          },
          data: {
            labels: ["Email Click Rate", "Email Open Rate", "In-App Interaction Rate", "Push Interaction Rate"],
            datasets: [{
              data: [
                state?.email_click_rate, 
                state?.email_open_rate, 
                state?.inapp_interaction_rate,
                state?.push_interaction_rate
              ],
              hoverOffset: 4,
              backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)',
                'rgb(122, 185, 21)'
              ]
            }]
          }
        }
      );
    })()
  }, [state])

  const retentionStrategyTypes = Object.keys(state?.retention_strategies)
  console.log('@@ ', retentionStrategyTypes?.length)

  return (
    <div className='main-app p-6 min-h-[1000px]'>
      <Link to='/insights' state={JSON.parse(localStorage.getItem('insights-data'))}>
        <button className='cursor-pointer transition duration-200 rounded-lg p-1 mb-4 bg-white hover:bg-gray-300'>
          <ChevronLeft />
        </button>
      </Link>

      <div className='mb-8'>
        <h3 className='text-white font-semibold mb-2 text-3xl'>
          <motion.span
            initial={{ opacity: 0.0, y: 150 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{
                duration: 1,
                ease: 'easeInOut'
            }}
          >
            {user_name}&apos;s Insights
          </motion.span>
        </h3>
        <motion.span 
          className='text-white font-extralight'
          initial={{ opacity: 0.0, y: 150 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
              delay: 0.2,
              duration: 1,
              ease: 'easeInOut'
          }}
        >
          Explore key metrics and behavioral trends to better understand your users.
        </motion.span>
      </div>

      <div className='grid grid-cols-2 sm:grid-cols-3 gap-3'>
        <motion.div 
          className='bg-white/20 p-4 backdrop-blur-lg backdrop-filter rounded-lg'
          initial={{ opacity: 0.0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
              duration: 1,
              delay: 0.3,
              ease: 'easeInOut'
          }}
        >
          <h4 className='font-bold text-lg text-white'>Historical Data</h4>

          <div className='mt-4'>
            <div className='grid grid-cols-2 gap-3'>
              <div>
                <h5 className='text-white font-extralight mb-1 text-xs'>Email Click Rate</h5>
                <p className="text-white text-sm font-light">{state?.email_click_rate || '0'}</p>
              </div>
              <div>
                <h5 className='text-white font-extralight mb-1 text-xs'>Email Open Rate</h5>
                <p className="text-white text-sm font-light">{state?.email_open_rate || '0'}</p>
              </div>
              <div>
                <h5 className='text-white font-extralight mb-1 text-xs'>In-App Interaction Rate</h5>
                <p className="text-white text-sm font-light">{state?.inapp_interaction_rate || '0'}</p>
              </div>
              <div>
                <h5 className='text-white font-extralight mb-1 text-xs'>Push Interaction Rate</h5>
                <p className="text-white text-sm font-light">{state?.push_interaction_rate || '0'}</p>
              </div>
              <div>
                <h5 className='text-white font-extralight mb-1 text-xs'>Push Opt-In</h5>
                <p className="text-white text-sm font-light">{state?.push_opt_in ? 'Yes' : 'No'}</p>
              </div>

              {state?.churn_status && (
                <div>
                  <h5 className='text-white font-extralight mb-1 text-xs'>Churn Status</h5>
                  <div 
                    style={{ width: 'max-content' }} 
                    className={`churn churn--${churnTypes?.[churnStatusType]}`}
                  >
                    <div className='churn-status'>
                    </div>
                    <span>{churnTypeLabels?.[churnStatusType]}</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>

        <motion.div 
          className='bg-white/20 p-4 backdrop-blur-lg backdrop-filter rounded-lg'
          initial={{ opacity: 0.0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
              duration: 1,
              delay: 0.4,
              ease: 'easeInOut'
          }}
        >
          <canvas id='historical-data' className='h-[200px] w-full'></canvas>
        </motion.div>

        <motion.div 
          className='bg-white/20 p-4 backdrop-blur-lg backdrop-filter rounded-lg'
          initial={{ opacity: 0.0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
              duration: 1,
              delay: 0.5,
              ease: 'easeInOut'
          }}
        >
          <h4 className='font-bold text-lg text-white mb-2'>Reasons for Churning</h4>

          {Array.isArray(state?.churn_reasons) && state?.churn_reasons?.length === 0 && (
            <p>We found no risk of churn for this user. This is great!</p>
          )}

          {Array.isArray(state?.churn_reasons) ? state?.churn_reasons?.map((churnReason, idx) => {
            return (
              <p key={idx} className='text-white mb-1 text-sm font-light'>
                {idx + 1}. {churnReason}
              </p>
            )
          }) : <p>1. {state.churn_reasons}</p>}
        </motion.div>
      </div>

      <h3 className='text-white font-semibold mb-2 mt-12 text-3xl'>
        <motion.span
          initial={{ opacity: 0.0, y: 150 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{
              duration: 1,
              delay: 0.6,
              ease: 'easeInOut'
          }}
        >
          Retention Strategy
        </motion.span>
      </h3>
      <motion.span 
        className='text-white font-extralight'
        initial={{ opacity: 0.0, y: 150 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
            delay: 0.7,
            duration: 1,
            ease: 'easeInOut'
        }}
      >
        Explore ways to boost retention and engagement according to user behaviour and cultural preferences.
      </motion.span>
        
      <motion.div
        initial={{ opacity: 0.0, y: 150 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{
            delay: 0.8,
            duration: 1,
            ease: 'easeInOut'
        }}
      >
        <Tabs className='mt-4 mb-10' defaultValue={retentionStrategyTypes?.[0]}>
          <TabsList className={`grid grid-cols-${retentionStrategyTypes.length}`}>
            {retentionStrategyTypes.map((type) => (
              <TabsTrigger key={type} value={type}>
                {strategyLabels[type]}
              </TabsTrigger>
            ))}
          </TabsList>

          {retentionStrategyTypes.map((type) => {
            const strats = state?.retention_strategies?.[type]

            return (
              <TabsContent key={type} value={type}>
                <div className='grid grid-cols-3 max-h-[308px] gap-3'>
                  <div className='bg-white/20 p-4 backdrop-blur-lg backdrop-filter rounded-lg overflow-auto'>
                    <div>
                      <h4 className='text-sm font-normal text-white'>The Why</h4>
                      <p className='text-white font-thin'>
                        {Array.isArray(strats?.how) ? strats?.how?.[0] : strats?.how}
                      </p>

                      <h4 className='text-sm font-normal text-white mt-3'>The What</h4>
                      <p className='text-white font-thin'>
                        {Array.isArray(strats?.what) ? strats?.what?.[0] : strats?.what}
                      </p>

                      <h4 className='text-sm font-normal text-white mt-3'>The When</h4>
                      <p className='text-white font-thin'>
                        {Array.isArray(strats?.when) ? strats?.when?.[0] : strats?.when}
                      </p>
                    </div>
                  </div>

                  <div className='bg-white/20 p-4 backdrop-blur-lg backdrop-filter rounded-lg overflow-auto'>
                    <h4 className='font-bold text-lg text-white mb-2'>Suggested Cultural Content</h4>

                    {strats?.cultural_based_content?.map(({ content, date, event_name }) => (
                      <div key={event_name + date} className='mb-6'>
                        <h5 className='text-sm text-white'>{event_name}</h5>
                        <p className='text-white text-xs font-thin'>{new Date(date).toDateString()}</p>

                        <div className='text-white mt-3'>
                          {content}
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className='bg-white/20 p-4 backdrop-blur-lg backdrop-filter rounded-lg overflow-auto'>
                    <h4 className='font-bold text-lg text-white mb-2'>Suggested Regional Content</h4>

                    {strats?.regional_language_content?.map(({ content, language, event_name }) => (
                      <div key={event_name + language} className='mb-6'>
                        <h5 className='text-sm text-white'>{event_name}</h5>
                        <p className='text-white text-xs font-thin'>{language}</p>

                        <div className='text-white mt-1'>
                          {content}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </TabsContent>
            )
          })}
        </Tabs>
        </motion.div>
      </div>
  )
}
