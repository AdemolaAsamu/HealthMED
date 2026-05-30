import { motion } from 'framer-motion';

export default function BloodstreamAnimation() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8 },
    },
  };

  const teaspoonVariants = {
    float: {
      y: [0, -15, 0],
      transition: {
        duration: 3,
        repeat: Infinity,
        repeatType: 'reverse' as const,
      },
    },
    rotate: {
      rotate: [0, 360],
      transition: {
        duration: 4,
        repeat: Infinity,
      },
    },
  };

  return (
    <motion.div
      className="relative h-96 bg-gradient-to-b from-blue-50 to-blue-100 rounded-2xl overflow-hidden"
      variants={containerVariants}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true }}
    >
      {/* Background blood cells */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(8)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-3 h-3 bg-red-400 rounded-full opacity-20"
            animate={{
              x: ['-10%', '110%'],
              y: Math.sin(i) * 50 + 100,
            }}
            transition={{
              duration: 4 + i * 0.3,
              repeat: Infinity,
              ease: 'linear',
            }}
            style={{
              left: `${(i / 8) * 100}%`,
            }}
          />
        ))}
      </div>

      {/* Main teaspoon visualization */}
      <div className="absolute inset-0 flex flex-col items-center justify-center gap-8">
        {/* Glucose molecules (dots inside teaspoon) */}
        <motion.div
          className="relative w-32 h-40 bg-amber-100 rounded-b-3xl border-4 border-amber-400 flex items-center justify-center overflow-hidden"
          animate="float"
          variants={teaspoonVariants}
        >
          {/* Sugar crystals */}
          {[...Array(12)].map((_, i) => (
            <motion.div
              key={`sugar-${i}`}
              className="absolute w-1.5 h-1.5 bg-amber-500 rounded-full"
              animate={{
                y: [0, -20, 0],
                x: Math.sin(i) * 30,
              }}
              transition={{
                duration: 2 + (i % 3) * 0.5,
                repeat: Infinity,
                delay: i * 0.1,
              }}
              style={{
                left: `${50 + Math.cos(i) * 40}%`,
                top: `${50 + Math.sin(i) * 40}%`,
              }}
            />
          ))}

          {/* Teaspoon handle */}
          <div className="absolute -top-12 left-1/2 -translate-x-1/2 w-6 h-14 bg-gray-300 rounded-full" />
        </motion.div>

        {/* Teaspoon label */}
        <motion.div
          variants={itemVariants}
          className="text-center"
        >
          <p className="text-3xl font-bold text-brand-primary mb-2">
            ~4.5g Glucose
          </p>
          <p className="text-lg text-gray-600">
            Normal blood glucose (about 1 teaspoon)
          </p>
        </motion.div>

        {/* Flowing glucose particles animation */}
        <motion.div className="absolute bottom-20 left-1/2 -translate-x-1/2 w-64">
          <motion.div
            className="h-1 bg-gradient-to-r from-transparent via-glucose-elevated to-transparent rounded-full"
            animate={{
              opacity: [0, 1, 0],
              x: [-100, 100],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              delay: 0,
            }}
          />
        </motion.div>
      </div>

      {/* Comparison indicator */}
      <motion.div
        variants={itemVariants}
        className="absolute bottom-4 right-4 bg-white bg-opacity-90 p-3 rounded-lg text-sm font-semibold text-brand-dark"
      >
        <p>Typical meal: 30-100g+ carbs</p>
        <p className="text-brand-primary">= 7-22+ teaspoons!</p>
      </motion.div>
    </motion.div>
  );
}

