import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Zap, Brain, Heart } from 'lucide-react';
import BloodstreamAnimation from '@/components/landing/BloodstreamAnimation';

export default function Home() {
  const features = [
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Visualize Your Blood Sugar',
      description: 'See exactly how glucose enters and leaves your bloodstream',
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'Understand the Science',
      description: 'Learn why fiber, protein, and movement matter',
    },
    {
      icon: <Heart className="w-8 h-8" />,
      title: 'Optimize Your Health',
      description: 'Make informed food and lifestyle choices',
    },
  ];

  const stats = [
    { number: '~4.5g', label: 'Blood glucose in a teaspoon' },
    { number: '30-100g+', label: 'Carbs in a typical meal' },
    { number: '20-30%', label: 'Glucose reduction from walking' },
    { number: '7-9 hrs', label: 'Sleep needed for glucose control' },
  ];

  return (
    <div className="space-y-0">
      {/* Hero Section */}
      <section className="section bg-gradient-to-br from-brand-primary via-red-500 to-pink-500 text-white">
        <div className="container-responsive grid md:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              Your blood only carries <span className="text-brand-accent">1 teaspoon</span> of sugar
            </h1>
            <p className="text-xl mb-8 text-white text-opacity-90">
              So what happens when you eat 10 teaspoons in one meal?
            </p>
            <p className="text-lg mb-8 text-white text-opacity-80">
              Interactive visualization to understand glucose, insulin, and metabolic health
            </p>
            <div className="flex gap-4 flex-wrap">
              <Link to="/analyze" className="btn-primary flex items-center gap-2">
                Analyze a Meal <ArrowRight size={20} />
              </Link>
              <Link to="/learn" className="btn-secondary">
                Learn More
              </Link>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <BloodstreamAnimation />
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="section bg-white">
        <div className="container-responsive">
          <h2 className="text-4xl font-bold text-center mb-16">
            Key Facts About Blood Glucose
          </h2>
          <div className="grid md:grid-cols-4 gap-8">
            {stats.map((stat, idx) => (
              <motion.div
                key={idx}
                className="card text-center"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: idx * 0.1 }}
                viewport={{ once: true }}
              >
                <p className="text-4xl font-bold text-brand-primary mb-3">
                  {stat.number}
                </p>
                <p className="text-gray-600">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section bg-brand-light">
        <div className="container-responsive">
          <h2 className="text-4xl font-bold text-center mb-6">
            What You'll Learn
          </h2>
          <p className="text-xl text-center text-gray-600 mb-16 max-w-2xl mx-auto">
            Inside My Meal helps you understand the science behind how food affects your body.
            No medical jargon, just clear visualizations and honest education.
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <motion.div
                key={idx}
                className="card"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: idx * 0.1 }}
                viewport={{ once: true }}
              >
                <div className="w-16 h-16 bg-brand-primary bg-opacity-10 rounded-lg flex items-center justify-center mb-4 text-brand-primary">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="section bg-white">
        <div className="container-responsive">
          <h2 className="text-4xl font-bold text-center mb-16">
            How Inside My Meal Works
          </h2>
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {[
              {
                number: '1',
                title: 'Search Foods',
                description: 'Add any food you want to analyze with accurate nutrition data',
              },
              {
                number: '2',
                title: 'Adjust Lifestyle',
                description: 'Tell us about your activity, sleep, and meal timing',
              },
              {
                number: '3',
                title: 'See Results',
                description: 'Watch animated glucose curves and understand the impact',
              },
            ].map((step, idx) => (
              <motion.div
                key={idx}
                className="relative"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: idx * 0.1 }}
                viewport={{ once: true }}
              >
                <div className="card text-center">
                  <div className="w-12 h-12 bg-brand-primary text-white rounded-full flex items-center justify-center mx-auto mb-4 text-lg font-bold">
                    {step.number}
                  </div>
                  <h3 className="text-xl font-bold mb-2">{step.title}</h3>
                  <p className="text-gray-600">{step.description}</p>
                </div>
                {idx < 2 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                    <ArrowRight className="text-brand-primary" size={32} />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section bg-gradient-to-r from-brand-primary to-brand-secondary text-white">
        <div className="container-responsive text-center max-w-2xl mx-auto">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Understand Your Metabolism?
          </h2>
          <p className="text-xl mb-8 text-white text-opacity-90">
            Start by analyzing a meal and see how your body responds to different foods and lifestyle factors
          </p>
          <Link to="/analyze" className="btn-accent inline-flex items-center gap-2">
            Start Analyzing <ArrowRight size={20} />
          </Link>
        </div>
      </section>

      {/* Disclaimer Footer */}
      <section className="section bg-brand-dark text-white text-center">
        <div className="container-responsive max-w-3xl mx-auto">
          <p className="text-lg font-semibold mb-4">
            📋 Important Disclaimer
          </p>
          <p className="text-white text-opacity-80">
            Inside My Meal is an educational tool only and is NOT medical advice. Individual glucose responses vary significantly.
            Always consult with healthcare providers for medical guidance. This tool cannot replace professional medical evaluation or continuous glucose monitoring.
          </p>
        </div>
      </section>
    </div>
  );
}

